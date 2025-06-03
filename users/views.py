from django.contrib.auth import login
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from music.models import Song, Playlist
from .forms import BayouUserCreationForm, CustomLoginForm, BayouUserUpdateForm
from .models import BayouUser
from django.contrib.auth.models import Group


def home(request):
    # all songs
    songs = Song.objects.all()

    # latest playlists created
    latest_playlists = Playlist.objects.order_by('-id')[:5]

    # top songs at the moment
    top_songs = Song.objects.annotate(
        times_added=Count('playlists')
    ).order_by('-times_added')[:5]

    return render(request, 'home.html', {
        'songs': songs,
        'latest_playlists': latest_playlists,
        'top_songs': top_songs,
    })


def register(request):
    if request.method == 'POST':
        form = BayouUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            listener_group = Group.objects.get(name='Listener')
            user.groups.add(listener_group)

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

    if is_owner:
        if request.method == 'POST':
            form = BayouUserUpdateForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
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
    })