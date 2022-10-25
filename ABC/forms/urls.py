from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    path('', views.examples, name='examples'),
    path('<str:form_id>', views.show_form, name='show_form'),
]