from django.urls import path
from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:site_dir_name>', views.show_site, name='show_site'),
]