from django.urls import path
from . import views


app_name = 'image_store'

urlpatterns = [
    path('', views.index, name='index'),
    path('download_full_collection', views.download_full_collection),
    path('chosen_avatars', views.chosen_avatars, name='chosen_avatars'),
    path('download_chosen_avatars', views.download_chosen_avatars, name='download_chosen_avatars'),

    path('badges', views.badges, name='badges'),
    path('badges/<str:category>', views.badges_category, name='badges_category'),

    path('iframe', views.iframe, name='iframe'),
    path('load_images_by_urls', views.load_images_by_urls, name='load_images_by_urls'),
    path('edit_serts', views.edit_serts, name='edit_serts'),
    path('create_cert', views.create_cert, name='create_cert'),
]