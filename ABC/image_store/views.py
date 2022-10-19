import os
from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings
from .models import Avatar
# Create your views here.

def index(requests):
    avatars = Avatar.objects.all()
    content = {
        'avatars': avatars,
    }
    return render(requests, 'image_store/main.html', content)


def all(request):
    images = Avatar.objects.all()
    content = {
        'images': images,
    }
    return render(request, 'image_store/all.html', content)


def download_collection(requests):
    zip_path = 'avatars_zip/afro.zip'
    file_path = os.path.join(settings.MEDIA_ROOT, zip_path)
    print(file_path)
    response = FileResponse(open(file_path, 'rb'))
    return response