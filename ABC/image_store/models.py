from django.db import models
import io
import os
import uuid
import zipfile
import random as r
import requests as req
from PIL import Image
from django.core.files.images import ImageFile
from django.contrib import admin
from django.utils.html import format_html
from rembg import remove

from PIL import ImageFont
from PIL import ImageDraw
from django.core.files import File


import shutil

def get_random_archive_name():
    symbols = 'qwertyuiopasdfghjklzxcvbnm'
    res = ''
    for char in range(8):
        char = r.choice(symbols)
        if r.randint(0,1):
            char = char.upper()
        res += char
    return res

def get_color(rgb_color):
    colors = rgb_color[4:-1].split(', ')
    return list(map(int,colors))

def copy_file(path):
    path_to_make_copy = '/home/vlad/WORK/badges'
    file_name = os.path.basename(path)
    dst = os.path.join(path_to_make_copy, file_name)
    shutil.copyfile(path, dst)


def load_img_like_bytes(img_url, img_name=str(uuid.uuid4())):
    file_ext = os.path.splitext(img_url)[-1]
    IMAGE_NAME = img_name + file_ext
    res = req.get(img_url)
    if res.status_code == 200:
        image_bytes = res.content
        return ImageFile(io.BytesIO(image_bytes), name=IMAGE_NAME)
    else:
        print('Error', res.status_code, img_url)



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

    def save(self, *args, **kwargs):
        if not self.pk:
            name, ext = os.path.splitext(self.image.name)
            self.image.name = str(uuid.uuid4()) + ext
        super().save()

    @staticmethod
    def load_from_url(url, sex='', category=None):
        img = load_img_like_bytes(url)
        geo = GeoGroup.objects.get(eng_name=category)
        if img:
            avatar = Avatar(
                image=img,
                sex=sex,
                category=geo
            )
            avatar.save()
            print(avatar, url)
            return avatar
        else:
            print('NO save', url)
            return False


class Certificate(models.Model):
    image = models.ImageField(upload_to='certificates')

    @staticmethod
    def load_from_url(url):
        img = load_img_like_bytes(url)
        if img:
            cert = Certificate()
            cert.image = img
            cert.save()
            return cert
        else:
            return False

    def add_text_on_image(self, font_zoom, text_blocks):
        FONT_FIX = 0.9
        img = Image.open(self.image.path).convert('RGBA')
        txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
        for cert_text in self.certtext_set.all():
            text_data = text_blocks[str(cert_text.pk)]
            WIDTH = cert_text.left  # left
            HEIGHT = cert_text.top  # top
            font_size = int(text_data['font-size'].replace('px', ''))
            FONT_SIZE = int(font_size * float(font_zoom) * FONT_FIX)
            COLOR = get_color(text_data['color'])
            opacity = int(float(text_data['opacity']) * 255)
            COLOR.append(opacity)
            COLOR = tuple(COLOR)
            TEXT = text_data['text']
            draw = ImageDraw.Draw(txt)
            draw.point((WIDTH, HEIGHT), fill=(0, 255, 0))
            font_model = Font.objects.get(name=text_data['font-family'])
            font = ImageFont.truetype(font_model.file.path, FONT_SIZE)
            left, top, width, heigth = font.getbbox(TEXT)
            draw.text((WIDTH - width / 2, HEIGHT - heigth / 2), TEXT, fill=COLOR, font=font)
        combined = Image.alpha_composite(img, txt)
        path_to_save = f'media/certificates_temp/{uuid.uuid4()}.png'
        combined.save(path_to_save)
        return path_to_save



class CertText(models.Model):
    text = models.CharField(max_length=255, default='Text')
    font_family = models.ForeignKey('Font', on_delete=models.PROTECT)
    font_size = models.IntegerField(default=30)
    opacity = models.FloatField(default=1)
    color = models.CharField(max_length=10, default='black')
    top = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    cert = models.ForeignKey(Certificate, on_delete=models.CASCADE)

class Badge(models.Model):
    OTHER  = 'other'
    CATEGORY = (
        ['100%', '100%'],
        ['discount', 'Скидки'],
        ['approved', 'Approved'],
        ['medical', 'Медицина'],
        ['social-network', 'Социальные сети и сервисы'],
        ['quality', 'Качество'],
        ['check', 'Галочки'],
        ['money', 'Деньги'],
        ['chat', 'Коментарии и чат'],
        ['charts', 'Графики'],
        ['free', 'Бесплатно'],
        ['number_one', 'Номер 1'],
        [OTHER, 'Прочее'],
    )

    BADGES_DIR = 'badges'
    image = models.ImageField(upload_to=BADGES_DIR)
    type = models.CharField(max_length=30, choices=CATEGORY, default=OTHER)

    class Meta:
        ordering = ['-pk']

    @staticmethod
    def load_from_url(url, type=None):
        if not type:
            type = Badge.OTHER
        img = load_img_like_bytes(url)
        if img:
            badge = Badge()
            badge.image = img
            badge.type = type
            badge.save()
            return badge
        else:
            return False

    @admin.display
    def image_prew(self):
        return format_html(
            '<img src="{}" / style="width:{}px;height: {}px;background-color: #db7575">',
            self.image.url,
            80,80,
        )

    def remove_background(self):
        copy_file(self.image.path)
        input_path = self.image.path
        output_path = self.image.path
        # print(input_path)
        input = Image.open(input_path)
        output = remove(input)
        #
        if self.image.path.endswith('.jpg'):
            self.image.name = self.image.name.replace('.jpg', '.png')
            output_path = output_path.replace('.jpg', '.png')
        #
        output.save(output_path)
        self.save()


class Font(models.Model):
    name = models.CharField(max_length=50, blank=True)
    file = models.FileField(upload_to='fonts')
    icon = models.ImageField(upload_to='fonts/images', blank=True)

    def __str__(self):
        return self.name



    def save(self, **kwargs):
        if not self.pk:
            super().save(**kwargs)
            self.create_font_img()
            self.get_font_name()
        else:
            super().save(**kwargs)

    def get_font_name(self):
        file =  os.path.basename(self.file.path)
        file_name, ext = os.path.splitext(file)
        self.name = file_name
        self.save()

    def create_font_img(self):
        BORDER_SIZE = 20
        FONT_SIZE = 80
        BACKGROUND_COLOR = (255, 255, 255)
        TEXT_COLOR = (0, 0, 0)
        TEXT = 'Ag'
        font = ImageFont.truetype(self.file.path, FONT_SIZE)
        left, top, width, heigth = font.getbbox(TEXT)
        if width > heigth:
            W_DIFF = 0
            H_DIFF = abs(width - heigth)
        else:
            W_DIFF = abs(width - heigth)
            H_DIFF = 0
        img_size = max(width, heigth) + BORDER_SIZE
        img = Image.new('RGB', (img_size, img_size), color=BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        draw.text((BORDER_SIZE / 2 + W_DIFF / 2, BORDER_SIZE / 2 + H_DIFF / 2), TEXT, TEXT_COLOR, font=font)
        blob = io.BytesIO()
        img.save(blob, 'JPEG')
        self.icon = File(blob, 'name.jpg')
        self.save()
        # img_path = f"./img_prew/{font_data['name']}.jpg"
        # img.save(img_path)
        # return img_path


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
