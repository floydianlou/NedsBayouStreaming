import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile

def crop_image_to_square(image_field, skip_keyword=None):
    try:
        if image_field and hasattr(image_field, 'file'):
            if skip_keyword and skip_keyword in str(image_field):
                return

            img = Image.open(image_field.file)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side

            img_cropped = img.crop((left, top, right, bottom))

            buffer = BytesIO()
            img_cropped.save(buffer, format='JPEG')
            buffer.seek(0)

            filename_only = Path(image_field.name).name
            image_field.save(
                filename_only,
                ContentFile(buffer.read()),
                save=False
            )

    except Exception as e:
        print("Error cropping image:", e)


def crop_image_to_169(image_field, skip_filename=None):
    try:
        if (
            image_field and
            hasattr(image_field, 'path') and
            os.path.exists(image_field.path)
        ):
            if skip_filename and os.path.basename(image_field.name) == skip_filename:
                return

            img = Image.open(image_field.path)
            target_ratio = 16 / 9
            current_ratio = img.width / img.height

            if current_ratio > target_ratio:
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                top = 0
                right = left + new_width
                bottom = img.height
            else:
                new_height = int(img.width / target_ratio)
                left = 0
                top = (img.height - new_height) // 2
                right = img.width
                bottom = top + new_height

            img_cropped = img.crop((left, top, right, bottom))
            img_cropped.save(image_field.path)
    except Exception as e:
        print("Error cropping image:", e)

def get_profile_picture_url(user):
    default_url = "https://res.cloudinary.com/dliev5zuy/image/upload/f_auto/v1750204693/defaultPicture_z9uqh8"

    try:
        url = user.profile_picture.url
    except Exception:
        url = default_url
    if '/upload/' in url and 'f_auto' not in url:
           url = url.replace('/upload/', '/upload/f_auto/')
    return url

def get_cover_url(cover_field):
    default_url = "https://res.cloudinary.com/dliev5zuy/image/upload/f_auto,c_fill,g_auto,w_100,h_100/v1750248957/defaultPlaylistCover_elb8ew.jpg"

    try:
        url = cover_field.url
    except:
        return default_url

    if '/upload/' in url:
        return url.replace('/upload/', '/upload/f_auto,c_fill/')
    return url

def get_artist_photo_url(artist):
    default_url = "https://res.cloudinary.com/dliev5zuy/image/upload/v1750249305/default_artist_vtyuz5.png"

    try:
        url = artist.photo.url
    except Exception:
        url = default_url
    if '/upload/' in url and 'f_auto' not in url:
        url = url.replace('/upload/', '/upload/f_auto/')
    return url