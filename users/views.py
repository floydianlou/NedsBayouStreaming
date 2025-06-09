from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from music.models import Song, Playlist
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