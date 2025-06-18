import os
from urllib.request import urlopen

from PIL import Image
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from phonenumber_field.modelfields import PhoneNumberField
from common_functions.utils import crop_image_to_square
from django.db import models

def default_profile_pic():
    return 'profile_pics/defaultPicture.png'

class BayouUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        storage=MediaCloudinaryStorage(),
        blank=True
    )
    short_bio = models.TextField(blank=True)
    phone_number = PhoneNumberField(blank=True, unique=True, region="IT")
    favorite_artist = models.ForeignKey('music.Artist', on_delete=models.SET_NULL, null=True, blank=True)
    liked_songs = models.ManyToManyField('music.Song', related_name='liked_by', blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.profile_picture:
            default_url = "https://res.cloudinary.com/dliev5zuy/image/upload/v1750204693/defaultPicture_z9uqh8.png"
            response = urlopen(default_url)
            image_data = response.read()
            self.profile_picture.save("defaultPicture.png", ContentFile(image_data), save=False)
        super().save(*args, **kwargs)