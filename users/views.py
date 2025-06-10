from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When, Value, IntegerField
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from music.models import Song, Playlist, Artist, Recommendation
from music.recommendations_utilities import update_recommendations
from music.views import generate_recommendations
from .forms import BayouUserCreationForm, CustomLoginForm, BayouUserUpdateForm
from .models import BayouUser


def home(request):
    # 10 random songs
    songs = Song.objects.order_by('?')[:8]

    # latest playlists created
    latest_playlists = Playlist.objects.order_by('-id')[:5]

    # top songs at the moment
    top_songs = Song.objects.annotate(
        times_added=Count('playlists')
    ).order_by('-times_added')[:5]

    # recommended preview
    suggestions = generate_recommendations(request.user)
    preview_artist = suggestions["related_artists"][0] if suggestions["related_artists"] else None
    preview_songs = suggestions["recommended_songs"][:3] if suggestions["recommended_songs"] else []

    return render(request, 'home.html', {
        'songs': songs,
        'latest_playlists': latest_playlists,
        'top_songs': top_songs,
        'preview_artist': preview_artist,
        'preview_songs': preview_songs,
    })

def register(request):
    if request.method == 'POST':
        form = BayouUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            listener_group = Group.objects.get(name='Listener')
            user.groups.add(listener_group)

            if user.favorite_artist:
                favorite_artist_songs = user.favorite_artist.song_set.all()
                if favorite_artist_songs.exists():
                    song = favorite_artist_songs.first()
                    update_recommendations(user, song=song, delta=5)

            return redirect('home')
    else:
        form = BayouUserCreationForm()
    return render(request, 'register.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


def profileView(request, username):
    user_profile = get_object_or_404(BayouUser, username=username)
    is_owner = request.user.is_authenticated and request.user.username == username

    playlists = user_profile.playlists.all()
    liked_songs = user_profile.liked_songs.select_related('artist').all()

    if is_owner:
        if request.method == 'POST':
            old_favorite = user_profile.favorite_artist
            form = BayouUserUpdateForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()

                # If favorite artist has changed, update recommendations accordingly
                if user_profile.favorite_artist != old_favorite:
                    # Remove 5 points from old favorite (if exists)
                    if old_favorite:
                        old_artist_songs = old_favorite.songs.all()
                        if old_artist_songs.exists():
                            first_song = old_artist_songs.first()
                            update_recommendations(user_profile, song=first_song, delta=-5)

                    # Add 5 points to new favorite (if exists)
                    if user_profile.favorite_artist:
                        favorite_artist_songs = user_profile.favorite_artist.songs.all()
                        if favorite_artist_songs.exists():
                            first_song = favorite_artist_songs.first()
                            update_recommendations(user_profile, song=first_song, delta=5)

                return redirect('profile', username=username)
        else:
            form = BayouUserUpdateForm(instance=user_profile)
    else:
        form = None

    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'is_owner': is_owner,
        'form': form,
        'playlists': playlists,
        'liked_songs': liked_songs,
    })

@login_required
def toggle_like_song(request, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        user = request.user

        liked = False
        if song in user.liked_songs.all():
            user.liked_songs.remove(song)
            update_recommendations(user, song, -3)
        else:
            user.liked_songs.add(song)
            update_recommendations(user, song, 3)
            liked = True
        return JsonResponse({'liked': liked})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def build_match_score(field, top_genres):
    return Case(
        *(When(**{field: genre}, then=Value(score)) for genre, score in zip(top_genres, [3, 2, 1])),
        default=Value(0),
        output_field=IntegerField()
    )

def search_results_view(request):
    query = request.GET.get('q', '')
    print("📥 QUERY ricevuta:", query)

    top_genres_ordered = []

    if request.user.is_authenticated:
        print("✅ Utente autenticato:", request.user.username)

        top_recommendations = Recommendation.objects.filter(
            user=request.user, score__gt=0
        ).order_by('-score')[:3]

        print("📊 Recommendation trovate:", top_recommendations)

        top_genres_ordered = [rec.genre for rec in top_recommendations]

        print("🏆 Top generi ordinati:")
        for i, genre in enumerate(top_genres_ordered):
            print(f"  {i+1}. {genre.name}")
    else:
        print("⛔ Utente non autenticato")

        # === SONGS ===
    songs_qs = Song.objects.filter(title__icontains=query)

    if top_genres_ordered:
        print("🎶 Filtro per canzoni nei top generi attivo!")

        songs_top = songs_qs.filter(artist__genres__in=top_genres_ordered).annotate(
            match_score=build_match_score('artist__genres', top_genres_ordered)
        ).distinct().order_by('-match_score', 'title')

        songs_other = songs_qs.exclude(artist__genres__in=top_genres_ordered).order_by('title')
    else:
        print("🎵 Nessun top genere: tutte le canzoni sono 'other'")
        songs_top = Song.objects.none()
        songs_other = songs_qs.order_by('title')

    # === ARTISTS ===
    artists_qs = Artist.objects.filter(name__icontains=query)

    if top_genres_ordered:
        print("🧑‍🎤 Filtro per artisti nei top generi attivo!")

        artists_top = artists_qs.filter(genres__in=top_genres_ordered).annotate(
            match_score=build_match_score('genres', top_genres_ordered)
        ).distinct().order_by('-match_score', 'name')

        artists_other = artists_qs.exclude(genres__in=top_genres_ordered).distinct().order_by('name')
    else:
        print("🧑‍🎨 Nessun top genere: tutti gli artisti sono 'other'")
        artists_top = Artist.objects.none()
        artists_other = artists_qs.distinct().order_by('name')

    # === PLAYLIST & USER ===
    playlists = Playlist.objects.filter(name__icontains=query)
    users = BayouUser.objects.filter(username__icontains=query)

    is_personalized = bool(top_genres_ordered)

    print("📚 Playlist trovate:", list(playlists))
    print("👤 Utenti trovati:", list(users))

    context = {
        'query': query,
        'songs_top': songs_top,
        'songs_other': songs_other,
        'artists_top': artists_top,
        'artists_other': artists_other,
        'playlists': playlists,
        'users': users,
        'is_personalized': is_personalized,
    }

    return render(request, 'search_results.html', context)