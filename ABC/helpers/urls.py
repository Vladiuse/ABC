from django.urls import path
from . import views

app_name = 'helpers'

urlpatterns = [
    path('', views.index,),
    path('create_site_element_record', views.create_site_element_record, name='site_element_add'),
    path('site_elem_record/<str:elem_id>', views.site_elem_record, name='site_elem_record'),
]