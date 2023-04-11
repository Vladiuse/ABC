from django.contrib import admin
from .models import Avatar, GeoGroup, Certificate, Badge, Font, CertText, BadgeCategory
from django.utils.html import format_html, mark_safe


# Register your models here.

class AvatarAdmin(admin.ModelAdmin):
    list_display = ['id', 'sex', 'category']
    list_display_links = ['id', 'sex', 'category']
    list_filter = ['category']


class BadgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'image_prew', 'image']
    list_editable = ['type']

    actions = ['remove_background']

    @admin.action(description='Удалить фон')
    def remove_background(self, request, queryset):
        for badge in queryset:
            badge.remove_background()


class CertTextInline(admin.TabularInline):
    model = CertText

class CertificateAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_prew', 'editable']
    list_filter = ['editable']
    inlines = [
        CertTextInline,
    ]

    def image_prew(self, obj):
        # return mark_safe('<img src="{}" / style="width:{}px;height: {}px;>')
        return format_html(
            '<img src="{}" / style="width:{}px;height: {}px;"/>',
            obj.image.url,
            120,'auto',
        )

class FontAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image_prew']

    def image_prew(self, obj):
        return format_html(
            '<img src="{}" / style="width:{}px;height: {}px;"/>',
            obj.icon.url,
            120,'auto',
        )

admin.site.register(Avatar, AvatarAdmin)
admin.site.register(GeoGroup)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Font, FontAdmin)
admin.site.register(BadgeCategory)
