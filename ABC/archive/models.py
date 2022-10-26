from django.db import models
from django.conf import settings
import os
from zipfile import ZipFile
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your models here.



class Site(models.Model):

    SITES_DIR_PATH = os.path.join(settings.MEDIA_ROOT, 'archive')
    ZIPS_PATH = os.path.join(settings.MEDIA_ROOT, 'archive_zips')

    dir_path = models.CharField(max_length=255, verbose_name='Пусть к папке сайта', unique=True)
    name = models.CharField(max_length=255, verbose_name='Название', blank=True)
    description = models.CharField(max_length=255, verbose_name='Описание', blank=True)
    zip_archive = models.FileField(blank=True, upload_to='archive_zips')
    preview = models.URLField(blank=True)


    def get_url(self):
        """получить ссылку на index.html сайта"""
        return f'/media/archive/{self.dir_path}/index.html'

    def create_zip(self):
        """Создать архив сайта"""
        dir_path = os.path.join(self.SITES_DIR_PATH, str(self.dir_path))
        zip_path_to_save = os.path.join(self.ZIPS_PATH, str(self.dir_path)) + '.zip'
        zip_file = ZipFile(zip_path_to_save, 'w')
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                path_in_zip = os.path.relpath(file_path, dir_path)
                zip_file.write(file_path, path_in_zip)
        zip_file.close()






# from archive.models import Site
# s = Site.objects.get(pk=1)


