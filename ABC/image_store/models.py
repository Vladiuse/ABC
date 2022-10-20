from django.db import models
import os
import uuid
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your models here.

class GeoGroup(models.Model):
    eng_name = models.CharField(max_length=40, verbose_name='eng', primary_key=True)
    name = models.CharField(max_length=40, verbose_name='Регион', unique=True)

    def __str__(self):
        return f'{self.eng_name}'

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
        ('18-30','18-30'),
        ('31-49','31-49'),
        ('50+', '50+'),
    ]


    image = models.ImageField(upload_to=get_avatar_save_path)
    category = models.ForeignKey(GeoGroup, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    sex = models.CharField(max_length=10, blank=True, choices=SEX)
    age = models.CharField(max_length=10, blank=True,choices=AGE)


    def delete(self):
        if os.path.exists(self.image.path):
            os.remove(self.image.path)
        super().delete()

    def save(self):
        name,ext = os.path.splitext(self.image.name)
        self.image.name = str(uuid.uuid4()) + ext
        super().save()

# from image_store.models import Avatar
# a = Avatar.objects.get(pk=621)
# a.add_thumbnails()