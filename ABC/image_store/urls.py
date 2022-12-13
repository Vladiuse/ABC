from django.urls import path
from . import views


app_name = 'image_store'
urlpatterns = [
    path('', views.index, name='index'),
    path('download_full_collection', views.download_full_collection),
    path('chosen_avatars', views.chosen_avatars, name='chosen_avatars'),
    path('download_chosen_avatars', views.download_chosen_avatars, name='download_chosen_avatars'),

    path('badges', views.badges, name='badges'),
]