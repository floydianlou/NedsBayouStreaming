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
                # Image is too wide → crop width
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                top = 0
                right = left + new_width
                bottom = img.height
            else:
                # Image is too tall → crop height
                new_height = int(img.width / target_ratio)
                left = 0
                top = (img.height - new_height) // 2
                right = img.width
                bottom = top + new_height

            img_cropped = img.crop((left, top, right, bottom))
            img_cropped.save(image_field.path)
    except Exception as e:
        print("Error cropping image:", e)