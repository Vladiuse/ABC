import os
import zipfile
from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings
from .models import Avatar, SexCounter, get_random_archive_name, Certificate, Badge
# Create your views here.
import random as r
from django.contrib.auth.decorators import login_required
from .iframe_viewer import Land
import requests as req


@login_required
def index(requests):
    avatars = Avatar.objects.all()
    content = {
        'avatars': avatars,
    }
    return render(requests, 'image_store/main.html', content)

@login_required
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


@login_required
def download_full_collection(requests, geo_group):
    """Скачать все аватарки конкретной группы стран"""
    zip_path = f'avatars_zip/{geo_group}.zip'
    file_path = os.path.join(settings.MEDIA_ROOT, zip_path)
    response = FileResponse(open(file_path, 'rb'))
    return response

@login_required
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


@login_required
def badges(requests):
    badges = Badge.objects.all()
    content = {
        'badges': badges,
    }
    return render(requests, 'image_store/badges.html', content)

@login_required
def certificates(request):
    FRAME_TYPES_COUNT = 6
    certs = Certificate.objects.all()
    for cert in certs:
        cert.frame_num = r.randint(1,FRAME_TYPES_COUNT)
    content = {
        'certs': certs,
    }
    return render(request, 'image_store/certificates/index.html', content)

def iframe(request):
    css_f  = open('image_store/iframe_viewer/styles.css')
    js_f = open('image_store/iframe_viewer/script.js')
    css_code = css_f.read()
    js_code = js_f.read()
    css_f.close()
    js_f.close()
    url = 'http://free2.inflax-new.com/'
    res = req.get(url)
    land = Land(res.text, url, parser='lxml')
    land.add_base_tag()
    land.add_script_tag(js_code)
    land.add_style_tag(css_code)
    html_code = str(land)
    html_code = land.escape_html_for_iframe(html_code)
    content = {
        'html_code': html_code,
        'original_url': Land.get_url_for_base_tag(url)
    }
    return render(request, 'image_store/iframe.html', content)

