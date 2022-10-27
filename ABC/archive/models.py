from django.db import models
from django.conf import settings
import os
from zipfile import ZipFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import Template
from django.template import Context

# Create your models here.
from django.conf import settings
import os


class Site(models.Model):
    ARCHIVE_DIR_NAME = 'archive'
    ARCHIVE_ZIPS_DIR_NAME = 'archive_zips'

    ARCHIVE_DIR_PATH = os.path.join(settings.MEDIA_ROOT, ARCHIVE_DIR_NAME)
    ZIPS_PATH = os.path.join(settings.MEDIA_ROOT, ARCHIVE_ZIPS_DIR_NAME)

    dir_name = models.CharField(max_length=255, verbose_name='Пусть к папке сайта', unique=True)
    name = models.CharField(max_length=255, verbose_name='Название', blank=True)
    description = models.CharField(max_length=255, verbose_name='Описание', blank=True)
    zip_archive = models.FileField(blank=True, upload_to='archive_zips')
    preview = models.URLField(blank=True)

    def get_url(self):
        """получить ссылку на index.html сайта"""
        return f'/media/{self.ARCHIVE_DIR_NAME}/{self.dir_name}/index.html'

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
        with open(self.index_path) as file:
            index = file.read()
        return index

    def render_template(self) -> str:
        """рендеринг сайта - добавление base и формы"""
        index_html = self._get_index_html_text()
        data = {
            'base_tag': self.get_base_tag()
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

# from archive.models import Site
# s = Site.objects.get(pk=1)
