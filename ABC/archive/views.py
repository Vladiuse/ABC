import os.path

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from .models import Site
from django.contrib.auth.decorators import login_required


# Create your views here.

countrys = [
    {'name': 'Россия', 'iso': 'ru', },
    {'name': 'Сербия', 'iso': 'rs', },
    {'name': 'Грузия', 'iso': 'ge', },
    {'name': 'Казахстан', 'iso': 'kz', },
    {'name': 'Украина', 'iso': 'ua', },
    {'name': 'Чехия', 'iso': 'cz', },
    {'name': 'Британия', 'iso': 'gb', },
    {'name': 'Польша', 'iso': 'pl', },
    {'name': 'Турция', 'iso': 'tr', },
    {'name': 'Сша', 'iso': 'us', },
    {'name': 'Мексика', 'iso': 'mx', },
    {'name': 'Босния', 'iso': 'ba', },
]

@login_required
def index(requests):
    sites = Site.objects.all()
    content = {
        'sites': sites,
        'countrys': countrys,
    }
    return render(requests, 'archive/index.html', content)

@login_required
def show_site(requests, dir_name):
    """Показать сайт"""
    site = get_object_or_404(Site, dir_name=dir_name)
    site_html = site.render_template()
    return HttpResponse(site_html)

@login_required
def site_load_zip(request, site_id):
    site = Site.objects.get(pk=site_id)
    file_name = os.path.basename(site.zip_archive.path)
    response = FileResponse(open(site.zip_archive.path, 'rb'), filename=file_name)
    return response