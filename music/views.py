from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from music.forms import PlaylistForm, PlaylistUpdateForm
from music.models import Song, Playlist


def song_catalogue_snippet(request):
    songs = Song.objects.select_related('artist', 'genre').all()
    return render(request, 'home.html', {'songs': songs})

@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.created_by = request.user
            playlist.save()
            form.save_m2m()
            return redirect('profile', username=request.user.username)
    else:
        form = PlaylistForm()
    return render(request, 'create_playlist.html', {'form': form})


def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    is_owner = request.user.is_authenticated and playlist.created_by == request.user

    if is_owner:
        if request.method == 'POST':
            form = PlaylistUpdateForm(request.POST, request.FILES, instance=playlist)
            if form.is_valid():
                form.save()
                return redirect('playlist_detail', playlist_id=playlist.id)
        else:
            form = PlaylistUpdateForm(instance=playlist)
    else:
        form = None

    return render(request, 'playlist_detail.html', {
        'playlist': playlist,
        'is_owner': is_owner,
        'form': form,
    })

@login_required
def delete_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)

    if playlist.created_by == request.user:
        playlist.delete()
        return redirect('profile', username=request.user.username)
    else:
        return redirect('playlist_detail', pk=pk)