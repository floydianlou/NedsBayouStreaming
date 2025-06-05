from django.urls import path
from . import views

urlpatterns = [
    path('create-playlist/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:pk>/delete/', views.delete_playlist, name='delete_playlist'),
    path('get_user_playlists/', views.get_user_playlists, name='get_user_playlists'),
    path('add_song_to_playlist/', views.add_song_to_playlist, name='add_song_to_playlist'),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
]
