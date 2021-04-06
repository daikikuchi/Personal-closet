from django.contrib import admin
from .models import Tag, Brand, Category, Shop, SubCategory


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    inlines = [SubCategoryInline]


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'url')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
