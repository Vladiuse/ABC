from django.db import models
import io
import os
import uuid
import zipfile
import random as r
import requests as req
from PIL import Image
from django.core.files.images import ImageFile

def get_random_archive_name():
    symbols = 'qwertyuiopasdfghjklzxcvbnm'
    res = ''
    for char in range(8):
        char = r.choice(symbols)
        if r.randint(0,1):
            char = char.upper()
        res += char
    return res


def load_img_like_bytes(img_url, img_name=str(uuid.uuid4())):
    file_ext = os.path.splitext(img_url)[-1]
    IMAGE_NAME = img_name + file_ext
    res = req.get(img_url)
    if res.status_code != 200:
        print('Eror')
    image_bytes = res.content
    return ImageFile(io.BytesIO(image_bytes), name=IMAGE_NAME)



class SexCounter:
    """
    Генерирует номер для картинки мужской или женской
    """

    def __init__(self):
        self.man = 0
        self.woman = 0
        self.other = 0

    def __call__(self, sex) -> str:
        if sex == 'man':
            self.man += 1
            return 'm' + str(self.man)
        elif sex == 'woman':
            self.woman += 1
            return 'w' + str(self.woman)
        else:
            self.other += 1
            return str(self.other)


class GeoGroup(models.Model):
    ZIPS_STORAGE = 'avatars_zip'

    eng_name = models.CharField(max_length=40, verbose_name='eng', primary_key=True)
    name = models.CharField(max_length=40, verbose_name='Регион', unique=True)
    zip = models.FileField(upload_to=ZIPS_STORAGE, verbose_name='Архив аватарок группы гео', blank=True)

    def __str__(self):
        return f'{self.eng_name}'

    def create_zip(self):
        """Создать архив с аватарками этой категории"""
        avatars = self.avatar_set.all()
        zip_file_name = f'media/{self.ZIPS_STORAGE}/{self.eng_name}.zip'
        zip_file = zipfile.ZipFile(zip_file_name, 'w')
        sex_counter = SexCounter()
        for avatar in avatars:
            file_name = os.path.basename(avatar.image.name)
            file_ext = os.path.splitext(file_name)[1]
            file_name_in_zip = sex_counter(avatar.sex) + file_ext
            zip_file.write(avatar.image.path, file_name_in_zip)
        zip_file.close()
        self.zip = f'{self.ZIPS_STORAGE}/{self.eng_name}.zip'
        self.save()


def get_avatar_save_path(instanse, filename):
    return f'avatars/{instanse.category}/{filename}'


class Avatar(models.Model):
    M = 'man'
    W = 'woman'
    NO = 'other'
    SEX = [
        (M, 'Мужской'),
        (W, 'Женский'),
        (NO, 'нет'),
    ]
    AGE = [
        ('18-30', '18-30'),
        ('31-49', '31-49'),
        ('50+', '50+'),
    ]

    TEMP_ZIPS_PATH = 'avatars_zip_tmp'

    image = models.ImageField(upload_to=get_avatar_save_path)
    category = models.ForeignKey(GeoGroup, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    sex = models.CharField(max_length=10, blank=True, choices=SEX)
    age = models.CharField(max_length=10, blank=True, choices=AGE)


    def delete(self):
        if os.path.exists(self.image.path):
            os.remove(self.image.path)
        super().delete()

    def save(self):
        name, ext = os.path.splitext(self.image.name)
        self.image.name = str(uuid.uuid4()) + ext
        super().save()

class Certificate(models.Model):
    image = models.ImageField(upload_to='certificates')

    @staticmethod
    def load_from_url(image_url):
        file_ext = os.path.splitext(image_url)[-1]
        IMAGE_NAME = str(uuid.uuid4()) + file_ext
        res = req.get(image_url)
        image_bytes = res.content
        certificate = Certificate()
        certificate.image = ImageFile(io.BytesIO(image_bytes), name=IMAGE_NAME)
        certificate.save()

class Badge(models.Model):
    BADGES_DIR = 'badges'
    image = models.ImageField(upload_to=BADGES_DIR)

    @staticmethod
    def load_from_url(url):
        b = Badge()
        b.image = load_img_like_bytes(url)
        b.save()

# import requests as req
# import os
# import uuid
#
# image_url = 'http://ug3.hondrostrong.com/img/header-creme.png'
# res = req.get(image_url)
# file_ext = os.path.splitext(image_url)[-1]
# IMAGE_NAME = str(uuid.uuid4()) + file_ext
# with open(IMAGE_NAME, 'wb') as file:
#     for chunk in res:
#         file.write(chunk)
