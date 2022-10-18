from django.contrib import admin
from .models import Avatar

# Register your models here.

class AvatarAdmin(admin.ModelAdmin):
    list_display = ['id', 'sex', 'category']
    list_display_links = ['id', 'sex', 'category']
    list_filter = ['category']

admin.site.register(Avatar, AvatarAdmin)