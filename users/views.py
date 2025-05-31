from django.contrib.auth import login
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import BayouUserCreationForm, CustomLoginForm


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