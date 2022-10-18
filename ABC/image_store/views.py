from django.shortcuts import render
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