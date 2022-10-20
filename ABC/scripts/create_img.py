"""
Подгрузка изображений в базу данных
"""



from image_store.models import Avatar, GeoGroup
import os
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


root = '/home/vlad/PycharmProjects/ABC/ABC/media/_avatars_to_load'
for dir_category in os.listdir(root):
    dir_path = os.path.join(root, dir_category)
    geo_group = GeoGroup.objects.get(pk=dir_category)
    for image in os.listdir(dir_path):
        image_path = os.path.join(dir_path, image)
        a = Avatar()
        image_name = os.path.basename(image_path)
        a.image = SimpleUploadedFile(name=image_name, content=open(image_path, 'rb').read(),
                                                   content_type=f'image/jpg')
        a.category = geo_group
        if image.startswith('m'):
            sex = 'man'
        else:
            sex = 'woman'
        a.sex = sex
        # i = Image.open(image_path)
        # i.load()
        # i.show()
        a.save()
