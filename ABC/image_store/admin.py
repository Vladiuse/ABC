from django.contrib import admin
from .models import Avatar, GeoGroup, Certificate, Badge

# Register your models here.

class AvatarAdmin(admin.ModelAdmin):
    list_display = ['id', 'sex', 'category']
    list_display_links = ['id', 'sex', 'category']
    list_filter = ['category']

admin.site.register(Avatar, AvatarAdmin)
admin.site.register(GeoGroup)
admin.site.register(Certificate)
admin.site.register(Badge)