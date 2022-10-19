from django.shortcuts import render
from .models import Site

# Create your views here.

def index(requests):
    sites = Site.objects.all()
    content = {
        'sites': sites
    }
    return render(requests, 'archive/index.html', content)
