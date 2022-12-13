from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Site


# Create your views here.

def index(requests):
    sites = Site.objects.all()
    content = {
        'sites': sites
    }
    return render(requests, 'archive/index.html', content)


def show_site(requests, site_dir_name):
    """Показать сайт"""
    site = get_object_or_404(Site, dir_name=site_dir_name)
    site_html = site.render_template()
    return HttpResponse(site_html)
