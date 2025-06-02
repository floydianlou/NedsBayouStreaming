import os

from music.utils import crop_image_to_square
from users.models import BayouUser
from PIL import Image
from django.db import models

def default_cover():
    return 'song_covers/default_cover.png'

def default_playlist_cover():
    return 'playlist_covers/default_cover.png'

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='artist_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    duration = models.DurationField(help_text="Format: HH:MM:SS")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='songs')
    cover = models.ImageField(upload_to='song_covers/', default=default_cover(), blank=True)

    def __str__(self):
        return f"{self.title} – {self.artist.name if self.artist else 'Artista sconosciuto'}"

    def save(self, *args, **kwargs):
        if not self.cover:
            self.cover = default_cover()

        super().save(*args, **kwargs)
        crop_image_to_square(self.cover, skip_filename='default_cover.png')

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(BayouUser, on_delete=models.CASCADE, related_name='playlists')
    cover = models.ImageField(
        upload_to='playlist_covers/',
        default=default_playlist_cover,
        blank=True
    )
    songs = models.ManyToManyField(Song, related_name="playlists", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.cover:
            self.cover = default_playlist_cover()

        super().save(*args, **kwargs)
        crop_image_to_square(self.cover, skip_filename='default_cover.png')