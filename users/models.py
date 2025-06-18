import os
from PIL import Image
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from common_functions.utils import crop_image_to_square
from django.db import models

from django.conf import settings
from django.core.files.storage import get_storage_class
print("📦 FILE STORAGE EFFETTIVO:", get_storage_class(settings.DEFAULT_FILE_STORAGE))

def default_profile_pic():
    return 'profile_pics/defaultPicture.png'

class BayouUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default=default_profile_pic,
        storage=MediaCloudinaryStorage(),
        blank=True
    )
    short_bio = models.TextField(blank=True)
    phone_number = PhoneNumberField(blank=True, unique=True, region="IT")
    favorite_artist = models.ForeignKey('music.Artist', on_delete=models.SET_NULL, null=True, blank=True)
    liked_songs = models.ManyToManyField('music.Song', related_name='liked_by', blank=True)

    def __str__(self):
        return self.username