from django.contrib import admin
from .models import Site





class SiteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'dir_name', 'country', 'original_url']
    list_display_links = ['name']
    actions = ['update_screenshots']

    @admin.action(description='Обновить скриншот')
    def update_screenshots(self, request, queryset):
        for site in queryset:
            site.create_screenshots()


admin.site.register(Site, SiteAdmin)
