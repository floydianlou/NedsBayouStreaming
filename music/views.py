from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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


def get_user_playlists(request):
    if request.user.is_authenticated:
        song_id = request.GET.get("song_id")
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return JsonResponse({"error": "Canzone non trovata"}, status=404)

        playlists = Playlist.objects.filter(created_by=request.user).exclude(songs=song)

        data = {
            "playlists": [
                {"id": p.id, "name": p.name}
                for p in playlists
            ]
        }
        return JsonResponse(data)

    else:
        return JsonResponse({"error": "Non autenticato"}, status=401)


@csrf_exempt
def add_song_to_playlist(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            playlist_id = data.get("playlist_id")
            song_id = data.get("song_id")

            playlist = Playlist.objects.get(id=playlist_id, user=request.user)
            song = Song.objects.get(id=song_id)

            playlist.songs.add(song)  # 🎯 Aggiunta!
            return JsonResponse({"success": True})

        except Playlist.DoesNotExist:
            return JsonResponse({"error": "Playlist non trovata."}, status=404)
        except Song.DoesNotExist:
            return JsonResponse({"error": "Canzone non trovata."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Richiesta non valida o utente non autenticato."}, status=400)

@require_POST
def add_song_to_playlist(request):
    try:
        data = json.loads(request.body)
        song_id = data.get("song_id")
        playlist_id = data.get("playlist_id")

        song = Song.objects.get(id=song_id)
        playlist = Playlist.objects.get(id=playlist_id)

        if request.user != playlist.created_by:
            return JsonResponse({"success": False, "error": "You do not own this playlist."})

        playlist.songs.add(song)
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})