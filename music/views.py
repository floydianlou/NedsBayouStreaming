from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from music.forms import PlaylistForm
from music.models import Song


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