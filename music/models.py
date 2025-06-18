from cloudinary.models import CloudinaryField
from users.models import BayouUser
from django.db import models

# DEFAULT COVERS FOR SONG, PLAYLIST AND ARTIST
def default_audio_file():
    return 'song_audio/13_Heavydirtysoul_Instrumental.mp3'


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
    photo = CloudinaryField(
        default="default_artist_vtyuz5.png",
        blank=True )
    genres = models.ManyToManyField('Genre', related_name='artists')

    def __str__(self):
        return self.name

# SONG MODEL
class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    audio_file = CloudinaryField(
        resource_type='video',
        default="HDS_-_DEMO_ldyoty.mp3",
        blank=True)
    cover = CloudinaryField(
        default="default_cover_td9qhw.png",
        blank=True)

    def __str__(self):
        return f"{self.title} – {self.artist.name if self.artist else 'Unknown artist'}"


# PLAYLIST MODEL
class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(BayouUser, on_delete=models.CASCADE, related_name='playlists')
    cover = CloudinaryField(
        default="defaultPlaylistCover_elb8ew.jpg",
        blank=True
    )
    songs = models.ManyToManyField(Song, related_name="playlists", blank=True)

    def __str__(self):
        return self.name

# RECOMMENDATION MODEL
class Recommendation(models.Model):
    user = models.ForeignKey(BayouUser, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'genre')

    def __str__(self):
        return f"{self.user.username} – {self.genre.name}: {self.score}"