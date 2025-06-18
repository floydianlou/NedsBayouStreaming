from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import json, random
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.views.generic import ListView, UpdateView

from common_functions.utils import get_cover_url, get_artist_photo_url, get_profile_picture_url, get_song_cover_url, \
    get_song_audio_url
from music.forms import PlaylistForm, PlaylistUpdateForm, GenreForm, ArtistAdminForm, SongForm
from music.models import Song, Playlist, Artist, Recommendation, Genre
from music.recommendations_utilities import update_recommendations, get_random_recommendations, get_random_songs, is_curator


# UPDATED
@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.created_by = request.user
            playlist.save()
            form.save_m2m()
            for song in form.cleaned_data['songs']:
                update_recommendations(request.user, artist=song.artist, delta=2)
            return redirect('profile', username=request.user.username)
    else:
        form = PlaylistForm()

    if request.user.is_authenticated:
        profile_picture_url = get_profile_picture_url(request.user)
    else:
        profile_picture_url = get_profile_picture_url(None)

    return render(request, 'create_playlist.html', {
        'form': form,
        'profile_picture_url': profile_picture_url,
    })

# UPDATED
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    playlist.cover_url = get_cover_url(playlist.cover)
    is_owner = request.user.is_authenticated and playlist.created_by == request.user

    if is_owner:
        if request.method == 'POST':
            form = PlaylistUpdateForm(request.POST, request.FILES, instance=playlist)
            if form.is_valid():
                # updates recommendation data removing points for removed songs and adding for new songs
                old_songs = set(playlist.songs.all())
                new_songs = set(form.cleaned_data['songs'])

                form.save()

                added_songs = new_songs - old_songs
                removed_songs = old_songs - new_songs

                for song in added_songs:
                    update_recommendations(request.user, artist=song.artist, delta=2)

                for song in removed_songs:
                    update_recommendations(request.user, artist=song.artist, delta=-2)

                return redirect('playlist_detail', playlist_id=playlist.id)
        else:
            form = PlaylistUpdateForm(instance=playlist)
    else:
        form = None

    playlist_songs = []

    for song in playlist.songs.all():
        song.cover_url = get_song_cover_url(song)
        song.audio_url = get_song_audio_url(song)
        playlist_songs.append(song)

    if request.user.is_authenticated:
        profile_picture_url = get_profile_picture_url(request.user)
    else:
        profile_picture_url = get_profile_picture_url(None)

    return render(request, 'playlist_detail.html', {
        'playlist': playlist,
        'songs': playlist_songs,
        'is_owner': is_owner,
        'form': form,
        'profile_picture_url': profile_picture_url,
    })

@login_required
def delete_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)

    if playlist.created_by == request.user:
        for song in playlist.songs.all():
            update_recommendations(request.user, artist=song.artist, delta=-2)
        playlist.delete()
        return redirect('profile', username=request.user.username)
    else:
        return redirect('playlist_detail', pk=pk)


def get_user_playlists(request):
    if request.user.is_authenticated:
        song_id = request.GET.get("song_id")
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return JsonResponse({"error": "Song not found"}, status=404)

        playlists = Playlist.objects.filter(created_by=request.user).exclude(songs=song)

        data = {
            "playlists": [
                {"id": p.id, "name": p.name}
                for p in playlists
            ]
        }
        return JsonResponse(data)

    else:
        return JsonResponse({"error": "Not logged in !!"}, status=401)

@require_POST
@login_required
def add_song_to_playlist(request):
    try:
        data = json.loads(request.body)
        song_id = data.get("song_id")
        playlist_id = data.get("playlist_id")

        song = Song.objects.get(id=song_id)
        playlist = Playlist.objects.get(id=playlist_id)

        if request.user != playlist.created_by:
            return JsonResponse({"success": False, "error": "You do not own this playlist."})

        # updates recommendations for added songs
        playlist.songs.add(song)
        update_recommendations(request.user, artist=song.artist, delta=2)
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    artist.photo_url = get_artist_photo_url(artist)
    all_songs = artist.songs.all()
    highlights = random.sample(list(all_songs), min(len(all_songs), 5))

    for song in all_songs:
        song.cover_url = get_song_cover_url(song)
        song.audio_url = get_song_audio_url(song)

    for song in highlights:
        song.cover_url = get_song_cover_url(song)
        song.audio_url = get_song_audio_url(song)

    if request.user.is_authenticated:
        profile_picture_url = get_profile_picture_url(request.user)
    else:
        profile_picture_url = get_profile_picture_url(None)

    return render(request, 'artist_detail.html', {
        'artist': artist,
        'highlights': highlights,
        'all_songs': all_songs,
        'profile_picture_url': profile_picture_url,
    })


# FUNCTION TO GET RECOMMENDED SONGS AND ARTISTS
def generate_recommendations(user):
    print(f"\nGENERATING RECOMMENDATIONS FOR: {user.username if user.is_authenticated else 'Unlogged user'}")

    # if user is unauthenticated or has no recommendation data yet, return random picks
    if not user.is_authenticated or not Recommendation.objects.filter(user=user, score__gt=0).exists():
        print("New user or unlogged user: returning random recommendations.")
        return get_random_recommendations(user)

    # retrieves top 3 favorite genres
    top_genres = Recommendation.objects.filter(user=user, score__gt=0).order_by('-score')[:3]
    top_genre_ids = [rec.genre.id for rec in top_genres]
    print("- Top Genres:")
    for rec in top_genres:
        print(f"  - {rec.genre.name}: {rec.score}")

    if not top_genres:
        # return random picks
        print("[NO TOP GENRES WITH POSITIVE SCORE] Using random recommendations.")
        return get_random_recommendations(user)

    # retrieves related artists ordered by number of common genres with user's top genres
    related_artists = (
        Artist.objects
        .filter(genres__in=top_genre_ids)
        .annotate(common_genres=Count('genres', filter=Q(genres__in=top_genre_ids)))
        .filter(common_genres__gt=0)
        .order_by('-common_genres')
    )

    print("- Related Artists Found:")
    for a in related_artists:
        print(f"  - {a.name} (common genres: {a.common_genres})")

    # selects top 2 related artists
    selected_related_artists = list(related_artists[:2])

    # if there are less than 2 related artists, fill with random artists
    if len(selected_related_artists) < 2:
        excluded_artist_ids = [a.id for a in selected_related_artists]
        filler_artists = Artist.objects.exclude(id__in=excluded_artist_ids)
        filler_list = list(filler_artists)
        random.shuffle(filler_list)
        selected_related_artists.extend(filler_list[:2 - len(selected_related_artists)])

    print("- Selected related artists:")
    for a in selected_related_artists:
        print(f"  - {a.name}")

    # select up to 5 songs from artists with genres matching top genres
    #  and excludes songs already liked by the user
    liked_artist_ids = user.liked_songs.values_list('artist__id', flat=True)
    candidate_songs = Song.objects.filter(
        Q(artist__genres__in=top_genre_ids) | Q(artist__id__in=liked_artist_ids)
    ).exclude(id__in=user.liked_songs.values_list('id', flat=True)).distinct()

    candidate_songs = list(candidate_songs)

    print("- Candidate Songs:")
    for s in candidate_songs:
        print(f"  - {s.title} by {s.artist.name}")

    # if no candidate songs available, fallback to random picks
    if not candidate_songs:
        recommended_songs = get_random_songs(user, 5)
    else:
        recommended_songs = random.sample(candidate_songs, min(5, len(candidate_songs)))

    print(f"-> Selected {len(recommended_songs)} recommended songs:")
    for s in recommended_songs:
        print(f"  - {s.title} by {s.artist.name}")

    # if less than 5 recommended songs, fill remaining slots with random songs
    if len(recommended_songs) < 5:
        missing = 5 - len(recommended_songs)
        print(f"Need to fill {missing} more song(s).")
        recommended_songs.extend(get_random_songs(user, missing, exclude_song_ids=[s.id for s in recommended_songs]))


    # --- RANDOM PART ---
    # select 1 random artist not already in the related artists list
    excluded_artist_ids = [a.id for a in selected_related_artists]
    if user.favorite_artist:
        excluded_artist_ids.append(user.favorite_artist.id)

    remaining_artists = Artist.objects.exclude(id__in=excluded_artist_ids)
    random_artist = random.choice(list(remaining_artists)) if remaining_artists.exists() else None
    if random_artist:
        print(f"- Random artist: {random_artist.name}")

    # select 2 random songs from remaining pool
    excluded_song_ids = [s.id for s in recommended_songs] + list(user.liked_songs.values_list('id', flat=True))
    remaining_songs = Song.objects.exclude(id__in=excluded_song_ids)

    remaining_songs_list = list(remaining_songs)

    if len(remaining_songs_list) < 2:
        print("Not enough unseen songs, using fallback.")
        fallback_candidates = list(
            Song.objects.exclude(id__in=[s.id for s in recommended_songs]))
        random.shuffle(fallback_candidates)
        random_songs = fallback_candidates[:2]
    else:
        random_songs = random.sample(remaining_songs_list, 2)

    print("- Random Songs:", [s.title for s in random_songs])

    return {
        "related_artists": selected_related_artists,
        "recommended_songs": recommended_songs,
        "random_artist": random_artist,
        "random_songs": random_songs
    }

# UPDATED
def recommendations_view(request):
    recs = generate_recommendations(request.user)

    for artist in recs['related_artists']:
        artist.photo_url = get_artist_photo_url(artist)

    if recs['random_artist']:
        recs['random_artist'].photo_url = get_artist_photo_url(recs['random_artist'])

    for song in recs['recommended_songs']:
        song.cover_url = get_song_cover_url(song)
        song.audio_url = get_song_audio_url(song)

    for song in recs['random_songs']:
        song.cover_url = get_song_cover_url(song)
        song.audio_url = get_song_audio_url(song)

    if request.user.is_authenticated:
        profile_picture_url = get_profile_picture_url(request.user)
    else:
        profile_picture_url = get_profile_picture_url(None)

    return render(request, 'recommendations.html', {
        'related_artists': recs['related_artists'],
        'recommended_songs': recs['recommended_songs'],
        'random_artist': recs['random_artist'],
        'random_songs': recs['random_songs'],
        'profile_picture_url': profile_picture_url,
    })


# LISTVIEW FOR REQUIREMENTS
# UPDATED
class SongListView(ListView):
    model = Song
    template_name = 'song_list.html'
    context_object_name = 'songs'
    ordering = ['artist__name', 'title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for song in context['songs']:
            song.cover_url = get_song_cover_url(song)
            song.audio_url = get_song_audio_url(song)

        if self.request.user.is_authenticated:
            context['profile_picture_url'] = get_profile_picture_url(self.request.user)
        else:
            context['profile_picture_url'] = get_profile_picture_url(None)

        return context


# UPDATED
@login_required
@user_passes_test(is_curator)
def curator_dashboard(request):
    genre_instance = None
    artist_instance = None
    song_instance = None

    if 'edit_genre' in request.GET:
        genre_instance = get_object_or_404(Genre, pk=request.GET['edit_genre'])
    if 'edit_artist' in request.GET:
        artist_instance = get_object_or_404(Artist, pk=request.GET['edit_artist'])
    if 'edit_song' in request.GET:
        song_instance = get_object_or_404(Song, pk=request.GET['edit_song'])

    genre_form = GenreForm(instance=genre_instance)
    artist_form = ArtistAdminForm(instance=artist_instance)
    song_form = SongForm(instance=song_instance)

    if request.method == 'POST':
        if 'genre_submit' in request.POST:
            genre_form = GenreForm(request.POST)
            if genre_form.is_valid():
                genre_form.save()
                messages.success(request, "Genre added successfully.")
                return redirect('curator_dashboard')

        elif 'genre_update' in request.POST:
            instance = get_object_or_404(Genre, pk=request.POST['genre_id'])
            genre_form = GenreForm(request.POST, instance=instance)
            if genre_form.is_valid():
                genre_form.save()
                messages.success(request, "Genre was updated correctly.")
                return redirect('curator_dashboard')

        elif 'artist_submit' in request.POST:
            artist_form = ArtistAdminForm(request.POST, request.FILES)
            if artist_form.is_valid():
                artist_form.save()
                messages.success(request, "Artist added successfully.")
                return redirect('curator_dashboard')

        elif 'artist_update' in request.POST:
            instance = get_object_or_404(Artist, pk=request.POST['artist_id'])
            artist_form = ArtistAdminForm(request.POST, request.FILES, instance=instance)
            if artist_form.is_valid():
                artist_form.save()
                messages.success(request, "Artist was updated correctly.")
                return redirect('curator_dashboard')

        elif 'song_submit' in request.POST:
            song_form = SongForm(request.POST, request.FILES)
            if song_form.is_valid():
                song_form.save()
                messages.success(request, "Song added successfully.")
                return redirect('curator_dashboard')
            else:
                for field, errors in song_form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        elif 'song_update' in request.POST:
            instance = get_object_or_404(Song, pk=request.POST['song_id'])
            song_form = SongForm(request.POST, request.FILES, instance=instance)
            if song_form.is_valid():
                song_form.save()
                messages.success(request, "Song was updated correctly.")
                return redirect('curator_dashboard')
            else:
                for field, errors in song_form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        elif 'delete_genre' in request.POST:
            genre_id = int(request.POST.get('genre_id'))
            genre = get_object_or_404(Genre, pk=genre_id)

            artists_to_delete = Artist.objects.annotate(
                genre_count=Count('genres')
            ).filter(genres=genre, genre_count=1)

            for artist in artists_to_delete:
                artist.delete()

            genre.delete()

            messages.success(request, f"Genre '{genre.name}' deleted along with {artists_to_delete.count()} artist(s).")
            return redirect('curator_dashboard')

        elif 'delete_artist' in request.POST:
            Artist.objects.filter(pk=request.POST.get('artist_id')).delete()
            messages.success(request, "Artist deleted.")
            return redirect('curator_dashboard')

        elif 'delete_song' in request.POST:
            Song.objects.filter(pk=request.POST.get('song_id')).delete()
            messages.success(request, "Song deleted.")
            return redirect('curator_dashboard')

    if request.user.is_authenticated:
        profile_picture_url = get_profile_picture_url(request.user)
    else:
        profile_picture_url = get_profile_picture_url(None)

    context = {
        'genre_form': genre_form,
        'artist_form': artist_form,
        'song_form': song_form,
        'genres': Genre.objects.all(),
        'artists': Artist.objects.all(),
        'songs': Song.objects.all(),
        'profile_picture_url': profile_picture_url,
    }
    return render(request, 'curator_dashboard.html', context)



