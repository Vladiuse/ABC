from django.shortcuts import render

def index(requests):
    return render(requests, 'image_store/index.html')