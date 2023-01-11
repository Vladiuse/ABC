from django.db import models
from uuid import uuid4
from django.conf import settings
import os
from zipfile import ZipFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import Template
from django.template import Context
from forms.models import FormExample
from django.core.files.storage import FileSystemStorage
import shutil
from archive.sreen_maker import ScreenMaker


# Create your models here.
from django.conf import settings
import os


class Site(models.Model):
    ARCHIVE_DIR_NAME = 'archive'
    ARCHIVE_ZIPS_DIR_NAME = 'archive_zips'
    THRASH = 'archive_removed'
    SCREENSHOTS_DIR = 'archive_screenshots'

    ARCHIVE_DIR_PATH = os.path.join(settings.MEDIA_ROOT, ARCHIVE_DIR_NAME)
    ZIPS_PATH = os.path.join(settings.MEDIA_ROOT, ARCHIVE_ZIPS_DIR_NAME)

    dir_name = models.CharField(max_length=255, verbose_name='Пусть к папке сайта', unique=True)
    name = models.CharField(max_length=255, verbose_name='Название', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    zip_archive = models.FileField(blank=True, upload_to=ARCHIVE_ZIPS_DIR_NAME)
    preview = models.URLField(blank=True)
    preview_mob = models.URLField(blank=True)
    phone_screenshot = models.ImageField(upload_to=SCREENSHOTS_DIR, blank=True, null=True)
    desktop_screenshot = models.ImageField(upload_to=SCREENSHOTS_DIR, blank=True, null=True)
    
    country = models.CharField(max_length=2, verbose_name='iso code', blank=True, )
    original_url = models.URLField(blank=True, verbose_name='ссылка на оригинальный сайт')

    def __str__(self):
        return str(self.dir_name)

    @property
    def thrash_dir_path(self):
        return FileSystemStorage().path(Site.THRASH)

    def delete(self):
        if FileSystemStorage().exists(self.dir_path):
            dir_local_path = FileSystemStorage().path(self.dir_path)
            new_name = f'{self.name}.{self.dir_name}.{uuid4()}'
            path_to_remove = os.path.join(self.thrash_dir_path,new_name)
            os.rename(dir_local_path, path_to_remove)
        super().delete()

    def create_screenshots(self):
        phone_screen_name = f'{self.dir_name}_ph_{uuid4()}.png'
        desktop_screen_name = f'{self.dir_name}_desk_{uuid4()}.png'
        path_to_save = FileSystemStorage().path(Site.SCREENSHOTS_DIR)
        driver = ScreenMaker()
        driver.get(self.get_local_url)
        driver.make_screenshot(
            screen_size=driver.PHONE,
            path_to_save=os.path.join(path_to_save, phone_screen_name),
        )
        driver.make_screenshot(
            screen_size=driver.DESKTOP,
            path_to_save=os.path.join(path_to_save, desktop_screen_name),
        )
        driver.quit()
        self.phone_screenshot = os.path.join(self.SCREENSHOTS_DIR, phone_screen_name)
        self.desktop_screenshot = os.path.join(self.SCREENSHOTS_DIR, desktop_screen_name)
        self.save()


    @property
    def dir_path(self):
        return os.path.join(Site.ARCHIVE_DIR_PATH, str(self.dir_name))

    @property
    def get_url(self) -> str:
        """получить ссылку на index.html сайта"""
        return f'/media/{self.ARCHIVE_DIR_NAME}/{self.dir_name}/index.html'

    @property
    def get_local_url(self):
        return 'http://127.0.0.1:8000' + self.get_url

    @property
    def base_tag_url(self):
        """Получить url для тэга base"""
        return f'/media/{self.ARCHIVE_DIR_NAME}/{self.dir_name}/'

    def get_base_tag(self):
        """Получить тэг <base>"""
        return f'<base href="{self.base_tag_url}">'

    @property
    def index_path(self) -> str:
        """Получить полный путь к index.html"""
        full_dir_path = os.path.join(settings.MEDIA_ROOT, str(self.ARCHIVE_DIR_PATH), str(self.dir_name))
        index_path = os.path.join(full_dir_path, 'index.html')
        return index_path

    def _get_index_html_text(self) -> str:
        """Возвращает текст index.html сайта"""
        with open(self.index_path, encoding='utf-8') as file:
            index = file.read()
        return index

    def render_template(self) -> str:
        """рендеринг сайта - добавление base и формы"""
        form = FormExample.objects.get(pk=2)

        index_html = self._get_index_html_text()
        data = {
            'base_tag': self.get_base_tag(),
            'form': form,
        }
        context = Context(data)
        template = Template(index_html)
        res = template.render(context)
        return str(res)

    def create_zip(self):
        """Создать архив сайта"""
        dir_path = os.path.join(self.ARCHIVE_DIR_PATH, str(self.dir_name))
        zip_path_to_save = os.path.join(self.ZIPS_PATH, str(self.dir_name)) + '.zip'
        zip_file = ZipFile(zip_path_to_save, 'w')
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                path_in_zip = os.path.relpath(file_path, dir_path)
                zip_file.write(file_path, path_in_zip)
        zip_file.close()

