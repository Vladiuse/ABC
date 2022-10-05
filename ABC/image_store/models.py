from django.db import models

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
    M = 'M'
    W = 'W'
    NO = 'NO'
    SEX = [
        (M, 'Мужской'),
        (W, 'Женский'),
        (NO, '-'),
    ]


    image = models.ImageField(upload_to='avatars')
    category = models.CharField(max_length=20, choices=RACE_CATEGORY)
    sex = models.CharField(max_length=2, blank=True, choices=SEX)

    # def save(self):
    #     self.image.name = '1.png'
    #     print(self.image.path)
    #     super().save()

