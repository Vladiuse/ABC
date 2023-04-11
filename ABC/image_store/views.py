import os
import zipfile
import json
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, JsonResponse
from django.conf import settings
from .models import Avatar, SexCounter, get_random_archive_name, Certificate, Badge, Font
# Create your views here.
import random as r
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .iframe_viewer import Land
import requests as req
from .forms import AvatarsAddForm, BadgeForm



@login_required
def index(requests):
    avatars = Avatar.objects.all()
    content = {
        'avatars': avatars,
    }
    return render(requests, 'image_store/avatars.html', content)

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
    # zip_file_path = f'media/{Avatar.TEMP_ZIPS_PATH}/{zipfile_name}.zip'
    zip_file_path = os.path.join(settings.MEDIA_ROOT, Avatar.TEMP_ZIPS_PATH, zipfile_name + '.zip')
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
    badges = Badge.objects.order_by('type').all()
    content = {
        'badges': badges,
        'range_16': range(16),
    }
    return render(requests, 'image_store/badges/badges.html', content)


@login_required
def badges_category(requests, category):
    for type, ru_name in Badge.CATEGORY:
        if ru_name == category:
            type = type
            break
    badges = Badge.objects.filter(type=type).order_by('type').all()
    content = {
        'badges': badges,
        'category': category,
    }
    return render(requests, 'image_store/badges/badges_category.html', content)

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

@csrf_exempt
def iframe(request):
    if request.method == 'POST':
        css_f  = open('image_store/iframe_viewer/styles.css')
        js_f = open('image_store/iframe_viewer/script.js')
        css_code = css_f.read()
        js_code = js_f.read()
        css_f.close()
        js_f.close()
        # url = 'http://free2.inflax-new.com/'
        url = request.POST['url']
        res = req.get(url)
        land = Land(res.text, url, parser='lxml')
        land.add_base_tag()
        land.add_script_tag(js_code)
        land.add_style_tag(css_code)
        html_code = str(land)
        html_code = land.escape_html_for_iframe(html_code)
        content = {
            'html_code': html_code,
            'original_url': Land.get_url_for_base_tag(url),
            'avatar_form': AvatarsAddForm(),
            'badge_form': BadgeForm(),
        }
        return render(request, 'image_store/iframe.html', content)
    else:
        return render(request, 'image_store/iframe_url_form.html')

def load_images_by_urls(request):
    load_result = []
    urls = request.POST['urls'].split(',')

    if request.POST['model'] == 'avatar':
        sex = request.POST['sex']
        category = request.POST['category']
        for url in urls:
            res = Avatar.load_from_url(url, sex=sex, category=category)
            load_result.append({'url': url, 'res': res})

    if request.POST['model'] == 'badge':
        type = request.POST['type']
        for url in urls:
            res = Badge.load_from_url(url, type=type)
            load_result.append({'url': url, 'res': res})

    if request.POST['model'] == 'certificate':
        print('LOAD CERTS')
        for url in urls:
            res = Certificate.load_from_url(url)
            load_result.append({'url': url, 'res': res})
    content = {
        'load_result': load_result,
    }
    return render(request, 'image_store/iframe_load_res.html', content)


def edit_cert(request):
    fonts = Font.objects.all()
    certificate = Certificate.objects.get(pk=request.GET['cert_id'])
    content = {
        'fonts': fonts,
        'certificate': certificate,
    }
    return render(request, 'image_store/certificates/online_editor.html', content)


@csrf_exempt
def create_cert(request):
    cert_id = request.POST['cert_id']
    font_zoom = request.POST['font_zoom']
    text_blocks = request.POST['text_blocks']
    try:
        cert = Certificate.objects.get(pk=cert_id)
        img_path = cert.add_text_on_image(font_zoom, json.loads(text_blocks))
        res = {
            'img_path': 'media/' + os.path.relpath(img_path,settings.MEDIA_ROOT),
        }
        return JsonResponse(res)
    except BaseException as error:
        return JsonResponse({
            'error': str(error),
        })
    # result = json.loads(text_blocks)
    # return JsonResponse(result, safe=False)

