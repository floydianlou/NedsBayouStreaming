from common_functions.utils import crop_image_to_square, crop_image_to_169
from mutagen import File as MutagenFile
from users.models import BayouUser
from django.db import models

# DEFAULT COVERS FOR SONG, PLAYLIST AND ARTIST
def default_audio_file():
    return 'song_audio/13_Heavydirtysoul_Instrumental.mp3'

def default_artist_photo():
    return 'artist_photos/default_artist.png'

def default_cover():
    return 'song_covers/default_cover.png'

def default_playlist_cover():
    return 'playlist_covers/defaultPlaylistCover.png'

# ----------------------------------------------------------

# GENRE MODEL
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# ARTIST MODEL
class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='artist_photos/', default=default_artist_photo(), blank=True)
    genres = models.ManyToManyField('Genre', related_name='artists')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.photo:
            self.photo = default_artist_photo()

        super().save(*args, **kwargs)
        crop_image_to_169(self.photo, skip_filename='default_artist.png')


# SONG MODEL (WITH IMAGE CROPPING)
class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    audio_file = models.FileField(upload_to='song_audio/', default=default_audio_file)
    cover = models.ImageField(upload_to='song_covers/', default=default_cover(), blank=True)

    def __str__(self):
        return f"{self.title} – {self.artist.name if self.artist else 'Unknown artist'}"

    def save(self, *args, **kwargs):
        if not self.cover:
            self.cover = default_cover()

        super().save(*args, **kwargs)

        crop_image_to_square(self.cover, skip_filename='default_cover.png')

# PLAYLIST MODEL (WITH IMAGE CROPPING)
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
        crop_image_to_square(self.cover, skip_filename='defaultPlaylistCover.png')

# RECOMMENDATION MODEL
class Recommendation(models.Model):
    user = models.ForeignKey(BayouUser, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'genre')

    def __str__(self):
        return f"{self.user.username} – {self.genre.name}: {self.score}"