from django.contrib import admin
from .models import FormExample, CasinoExample


class FormExampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'color','image_prew']
    list_editable = ['color']

# Register your models here.
class CasinoExampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'type','image_prew']
    list_editable = ['type']

admin.site.register(FormExample, FormExampleAdmin)
admin.site.register(CasinoExample, CasinoExampleAdmin)
