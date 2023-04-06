from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    path('examples', views.examples, name='examples'),
    path('casino', views.casino, name='casino'),
    path('examples/<str:form_id>', views.show_form, name='show_form'),
    path('form_localization', views.form_localization, name='form_localization'),
]