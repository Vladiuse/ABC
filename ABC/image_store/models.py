from django.db import models
import os
# Create your models here.

class Avatar(models.Model):
    EUROPE_NORTH = 'europe-north'
    EUROPE_SOUTH = 'europe-south'
    ARABS = 'arabs'
    INDIA = 'india'
    TURKISH = 'turkish'
    LATAM = 'turkish'
    AFRICA = 'africa'
    ASIA = 'asia'
    PAPUA = 'papua'
    CENTRAL_ASIA = 'central_asia'
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


    image = models.ImageField(upload_to='avatars')
    category = models.CharField(max_length=20, choices=RACE_CATEGORY)
    sex = models.CharField(max_length=10, blank=True, choices=SEX)

    def delete(self):
        if os.path.exists(self.image.path):
            os.remove(self.image.path)
        super().delete()

    # def save(self):
    #     self.image.name = '1.png'
    #     print(self.image.path)
    #     super().save()

