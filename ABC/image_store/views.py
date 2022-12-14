import os
import zipfile
from io import BytesIO
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from django.conf import settings
from .models import Avatar, SexCounter, get_random_archive_name, Certificate
# Create your views here.
import random as r

def index(requests):
    avatars = Avatar.objects.all()
    content = {
        'avatars': avatars,
    }
    return render(requests, 'image_store/main.html', content)

def chosen_avatars(requests):
    """просмотр выбраных пользователем аватарок"""
    avatars_ids_str = requests.GET['avatars_ids']
    avatars_ids = avatars_ids_str.split(',')
    avatars = Avatar.objects.filter(id__in=avatars_ids)
    content = {
        'avatars': avatars,
        'avatars_ids': avatars_ids_str,
    }
    return render(requests, 'image_store/chosen_avatars.html', content)


def download_full_collection(requests, geo_group):
    """Скачать все аватарки конкретной группы стран"""
    zip_path = f'avatars_zip/{geo_group}.zip'
    file_path = os.path.join(settings.MEDIA_ROOT, zip_path)
    response = FileResponse(open(file_path, 'rb'))
    return response

def download_chosen_avatars(requests):
    """Возвращает архив по выбраным айди аватарок"""
    avatars_ids_str = requests.GET['avatars_ids']
    avatars_ids = avatars_ids_str.split(',')
    avatars = Avatar.objects.filter(id__in=avatars_ids)
    zipfile_name = get_random_archive_name()
    zip_file_path = f'media/{Avatar.TEMP_ZIPS_PATH}/{zipfile_name}.zip'
    zip_file = zipfile.ZipFile(zip_file_path, 'w')
    counter = SexCounter()
    for avatar in avatars:
        avatar_name_in_zip = counter(avatar.sex) + '.jpg'
        zip_file.write(avatar.image.path, avatar_name_in_zip)
    zip_file.close()
    response = FileResponse(open(zip_file_path, 'rb'), filename='avatars.zip')
    return response


def badges(requests):
    return render(requests, 'image_store/badges.html')

def certificates(request):
    certs = Certificate.objects.all()
    for cert in certs:
        cert.frame_num = r.randint(1,5)
    content = {
        'certs': certs,
    }
    return render(request, 'image_store/certificates/index.html', content)

