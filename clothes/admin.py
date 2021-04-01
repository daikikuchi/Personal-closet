from django.contrib import admin
from .models import Tag, Brand


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Brand, BrandAdmin)
