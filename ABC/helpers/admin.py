from django.contrib import admin
from .models import Site, Element, SiteElementRecord


class SiteElementAdmin(admin.TabularInline):
    model = SiteElementRecord
    extra = 0


class SiteAdmin(admin.ModelAdmin):
    inlines = [SiteElementAdmin]


class ElementAdmin(admin.ModelAdmin):
    inlines = [SiteElementAdmin]


admin.site.register(Site, SiteAdmin)
admin.site.register(Element, ElementAdmin)
