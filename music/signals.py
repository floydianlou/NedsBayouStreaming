from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Song
from users.models import BayouUser
from music.recommendations_utilities import update_recommendations

@receiver(pre_delete, sender=Song)
def update_recommendations_on_song_delete(sender, instance, **kwargs):
    users_liked = BayouUser.objects.filter(liked_songs=instance).distinct()
    for user in users_liked:
        update_recommendations(user, instance, delta=-3)

    users_playlist = BayouUser.objects.filter(playlists__songs=instance).distinct()
    for user in users_playlist:
        update_recommendations(user, instance, delta=-2)