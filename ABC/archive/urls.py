from django.urls import path
from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:dir_name>', views.show_site, name='show_site'),
    path('site_load_zip/<str:site_id>', views.site_load_zip, name='site_load_zip'),
]