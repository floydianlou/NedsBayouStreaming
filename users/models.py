import os
from PIL import Image
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

def default_profile_pic():
    return 'profile_pics/defaultPicture.png'

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

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = 'profile_pics/defaultPicture.png'  # sets default picture if there is none

        super().save(*args, **kwargs)

        try:
            if (
                    self.profile_picture and
                    hasattr(self.profile_picture, 'path') and
                    os.path.exists(self.profile_picture.path) and
                    os.path.basename(self.profile_picture.name) != 'defaultPicture.png'
            ):
                img = Image.open(self.profile_picture.path)
                min_side = min(img.width, img.height)
                left = (img.width - min_side) // 2
                top = (img.height - min_side) // 2
                right = left + min_side
                bottom = top + min_side

                img_cropped = img.crop((left, top, right, bottom))
                img_cropped.save(self.profile_picture.path)
        except Exception as e:
            print("Errore durante il crop immagine profilo:", e) # TODO english! <3