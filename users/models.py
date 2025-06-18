import os
from PIL import Image
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from common_functions.utils import crop_image_to_square
from django.db import models

def default_profile_pic():
    return 'https://res.cloudinary.com/dliev5zuy/image/upload/v1750204693/defaultPicture_z9uqh8.png'

class BayouUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default=default_profile_pic,
        blank=True
    )
    short_bio = models.TextField(blank=True)
    phone_number = PhoneNumberField(blank=True, unique=True, region="IT")
    favorite_artist = models.ForeignKey('music.Artist', on_delete=models.SET_NULL, null=True, blank=True)
    liked_songs = models.ManyToManyField('music.Song', related_name='liked_by', blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
     #   if not self.profile_picture:
      #      self.profile_picture = 'profile_pics/defaultPicture.png'

        super().save(*args, **kwargs)

       # crop_image_to_square(self.profile_picture, skip_filename='defaultPicture.png')