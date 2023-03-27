from django.contrib import admin
from .models import FormExample


class FormExampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
# Register your models here.
admin.site.register(FormExample, FormExampleAdmin)
