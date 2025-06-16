from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Song
from users.models import BayouUser
from music.recommendations_utilities import update_recommendations

# SIGNAL BEFORE DELETING A SONG FROM DATABASE TO UPDATE ALL USER RECOMMENDATIONS!!
@receiver(pre_delete, sender=Song)
def update_recommendations_on_song_delete(sender, instance, **kwargs):
    artist = instance.artist

    users_liked = BayouUser.objects.filter(liked_songs=instance).distinct()
    for user in users_liked:
        update_recommendations(user, artist=artist, delta=-3)

    users_playlist = BayouUser.objects.filter(playlists__songs=instance).distinct()
    for user in users_playlist:
        update_recommendations(user, artist=artist, delta=-2)