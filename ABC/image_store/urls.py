from django.urls import path
from . import views


app_name = 'image_store'
urlpatterns = [
    path('', views.index),
    path('all', views.all),
]