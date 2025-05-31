from django.contrib.auth.models import AbstractUser
from django.db import models

def default_profile_pic():
    return 'profile_pics/defaultPicture.png'

class BayouUser(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default=default_profile_pic,
        blank=True
    )
    short_bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    favorite_band = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username