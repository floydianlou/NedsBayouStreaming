from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import loginView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('search/', views.search_results_view, name='search_results'),
    path('<str:username>/', views.profileView, name='profile'),
    path('like/<int:song_id>/', views.toggle_like_song, name='toggle_like'), # here because it's in homepage
]

