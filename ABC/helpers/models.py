from django.db import models
from datetime import date
import requests as req
from PIL import Image
import io


def get_image_remote_size(url, show=False):
    # url = 'https://files.kaiten.ru/44437eef-ef60-4603-b666-0f0b4a54d635.png?name=pgum3.png'
    res = req.get(url)
    if res.status_code == 200:
        file = io.BytesIO(res.content)
        img = Image.open(file)
        if show:
            img.show()
        return img.size  # width height
    else:
        print('Error', res.status_code, url)
        return None


# Create your models here.

# class Book(models.Model):
#     name = models.CharField(max_length=20)
#     date = models.DateField(default=date.today())


class Element(models.Model):
    NEWS_SITE_TEMPLATE = 'news_site_template'
    OTHER_TEMPLATE = 'other_template'

    FORM = 'form'
    BUTTONS = 'buttons'
    BUTTON_EFFECT = 'button_effect'
    ICONS = 'icons'
    CERTIFICATE = 'certificate'
    BADGES = 'badges'
    QUIZ = 'quiz'
    COMMENTS = 'comments'
    SHOW_HIDE = 'show_hide'
    ROULETTE = 'roulette'
    TIMERS = 'timers'
    other = 'other'

    ELEMENT_TYPES = (
        (FORM, 'Формы'),
        (BUTTONS, 'Кнопки'),
        (BUTTON_EFFECT, 'Еффекты кнопок'),
        (ICONS, 'Иконки'),
        (CERTIFICATE, 'Сертификаты'),
        (BADGES, 'Бэйджы'),
        (QUIZ, 'Опросники'),
        (COMMENTS, 'Комментарии'),
        (SHOW_HIDE, 'Показать/скрыть'),
        (ROULETTE, 'Розыгрыши'),
        (TIMERS, 'Таймеры'),
        (other, 'Прочее'),
    )
    name = models.CharField(max_length=20, choices=ELEMENT_TYPES, primary_key=True,)

    def __str__(self):
        return str(self.get_name_display())


class Site(models.Model):
    url = models.URLField(primary_key=True)
    element = models.ManyToManyField(Element, related_name='site', related_query_name='sites', blank=True, through='SiteElementRecord')

    def __str__(self):
        return str(self.url)


class SiteElementRecord(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE,)
    element = models.ForeignKey(Element, on_delete=models.CASCADE,)
    is_collect = models.BooleanField(blank=True, default=False, verbose_name='Элементы собраны')

    class Meta:
        ordering = ['is_collect']


class KmaOffer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    logo = models.URLField(blank=True)

    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return f'<{self.id}> {self.name} Size({self.width},{self.height})'

    @staticmethod
    def load_logos_size_null():
        offers = KmaOffer.objects.filter(width__isnull=True)
        print('Offers to load', len(offers))
        count = len(offers)
        for offer in offers:
            offer.get_logo_url_sizes()
            count -= 1
            print('Left:', count)

    def get_logo_url_sizes(self):
        size = get_image_remote_size(self.logo)
        if size:
            width, height = size
            self.width = width
            self.height = height
            self.save()

            print('SUCCESS', self)

    def dif(self):
        _max = max(self.width, self.height)
        _min = min(self.width, self.height)
        dif = round(_max / _min, 2)
        return dif


