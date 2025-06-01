from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import BayouUserCreationForm, CustomLoginForm, BayouUserUpdateForm
from .models import BayouUser


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = BayouUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
        'form': form
    })