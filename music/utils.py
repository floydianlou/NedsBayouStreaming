import os
from PIL import Image

def crop_image_to_square(image_field, skip_filename=None):
    try:
        if (
            image_field and
            hasattr(image_field, 'path') and
            os.path.exists(image_field.path)
        ):
            if skip_filename and os.path.basename(image_field.name) == skip_filename:
                return

            img = Image.open(image_field.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side

            img_cropped = img.crop((left, top, right, bottom))
            img_cropped.save(image_field.path)
    except Exception as e:
        print("Error cropping image:", e)