from django.db import models
import os
import uuid
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your models here.

class Avatar(models.Model):
    EUROPE_NORTH = 'europe-north' #
    EUROPE_SOUTH = 'europe-south' #
    ARABS = 'arabs' #
    INDIA = 'india' #
    TURKISH = 'turkish' #
    LATAM = 'latam'
    AFRICA = 'afro' #
    ASIA = 'asia' #
    PAPUA = 'papua' #
    CENTRAL_ASIA = 'central_asia' #
    RACE_CATEGORY = [
        (EUROPE_NORTH, 'Европейцы'),
        (EUROPE_SOUTH, 'Южная европа'),
        (ARABS, 'Арабы'),
        (INDIA, 'Индейцы'),
        (TURKISH, 'Турки и албанцы'),
        (LATAM, 'Индийцы'),
        (AFRICA, 'Африка'),
        (ASIA, 'Азиаты'),
        (PAPUA, 'Папуасы'),
        (CENTRAL_ASIA, 'Центральная азия и кавказ'),
    ]
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


    image = models.ImageField(upload_to='avatars', )
    category = models.CharField(max_length=20, choices=RACE_CATEGORY)
    sex = models.CharField(max_length=10, blank=True, choices=SEX)
    age = models.CharField(max_length=10, blank=True,choices=AGE)


    def delete(self):
        if os.path.exists(self.image.path):
            os.remove(self.image.path)
        super().delete()

    # def add_thumbnails(self):
    #     """Создание миниатюр"""
    #     original = Image.open(self.original.path)
    #     original.load()
    #     #make square
    #     if original.width != original.height:
    #         size = min(original.size)
    #         original = original.crop((0, 0, size, size))
    #     for fext in ('jpg', 'webp'):
    #         for size in range(50,300, 50):
    #             size = int(size)
    #             image = original.convert('RGB')
    #             image = image.resize((size,size))
    #             path, cur_fext = os.path.splitext(self.original.path)
    #             thumb_path = f'{path}__x{size}.{fext}'
    #             image.save(thumb_path)
    #             # new_filename = os.path.basename(thumb_path)
    #             # field = SimpleUploadedFile(name=new_filename, content=open(thumb_path, 'rb').read(),
    #             #                                   content_type=f'image/{fext}')
    #
    # def get_thumbnail_url(self, fext,size):
    #     return f'{os.path.splitext(self.original.url)[0]}__x{size}.{fext}'
    #
    # def jpg_50(self):
    #     return self.get_thumbnail_url('jpg', 50)
    #
    # def jpg_100(self):
    #     return self.get_thumbnail_url('jpg', 100)
    #
    # def jpg_150(self):
    #     return self.get_thumbnail_url('jpg', 150)
    #
    # def jpg_200(self):
    #     return self.get_thumbnail_url('jpg', 200)
    #
    # def jpg_250(self):
    #     return self.get_thumbnail_url('jpg', 250)
    #
    # def webp_50(self):
    #     return self.get_thumbnail_url('webp', 50)
    #
    # def webp_100(self):
    #     return self.get_thumbnail_url('webp', 100)
    #
    # def webp_150(self):
    #     return self.get_thumbnail_url('webp', 150)
    #
    # def webp_200(self):
    #     return self.get_thumbnail_url('webp', 200)
    #
    # def webp_250(self):
    #     return self.get_thumbnail_url('webp', 250)
    #
    def save(self):
        name,ext = os.path.splitext(self.image.name)
        self.image.name = str(uuid.uuid4()) + ext
        super().save()

# from image_store.models import Avatar
# a = Avatar.objects.get(pk=621)
# a.add_thumbnails()