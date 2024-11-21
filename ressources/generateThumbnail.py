from PIL import Image
import os

original_images_folder = '../static/images'
thumbnail_folder = '../static/thumbnail'

if not os.path.exists(thumbnail_folder):
    os.makedirs(thumbnail_folder)

image_files = os.listdir(original_images_folder)

for image_file in image_files:
    if image_file.endswith('.png'):
        image_path = os.path.join(original_images_folder, image_file)
        thumbnail_path = os.path.join(thumbnail_folder, image_file)

        with Image.open(image_path) as img:
            img.thumbnail((30, 30))
            img.save(thumbnail_path)
