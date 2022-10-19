from django.urls import path
from . import views


app_name = 'image_store'
urlpatterns = [
    path('', views.index, name='index'),
    path('download_collection', views.download_collection),
]