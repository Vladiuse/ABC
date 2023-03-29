from django.contrib import admin
from .models import FormExample, CasinoExample

class FormExampleInline(admin.StackedInline):
    model = FormExample

class FormExampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'color','image_prew']
    list_editable = ['color']
    inlines = [FormExampleInline]

# Register your models here.
class CasinoExampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'type','image_prew']
    list_editable = ['type']

admin.site.register(FormExample, FormExampleAdmin)
admin.site.register(CasinoExample, CasinoExampleAdmin)
