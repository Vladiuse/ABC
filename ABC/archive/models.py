from django.db import models

# Create your models here.



class Site(models.Model):
    dir_path = models.CharField(max_length=255, verbose_name='Пусть к папке сайта', unique=True)
    name = models.CharField(max_length=255, verbose_name='Название', blank=True)
    description = models.CharField(max_length=255, verbose_name='Описание', blank=True)


    def get_url(self):
        return f'/media/archive/{self.dir_path}/index.html'