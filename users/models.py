from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class BayouUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = CloudinaryField(
        default='defaultPicture_z9uqh8.png',
        blank=True
    )
    short_bio = models.TextField(blank=True)
    phone_number = PhoneNumberField(blank=True, unique=True, region="IT")
    favorite_artist = models.ForeignKey('music.Artist', on_delete=models.SET_NULL, null=True, blank=True)
    liked_songs = models.ManyToManyField('music.Song', related_name='liked_by', blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)