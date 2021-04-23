import uuid
import os

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


def clothes_image_file_path(instance, filename):
    """Generate file path for new clothes image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('clothes/', filename)


class Tag(models.Model):
    """Tag to be used for clothes"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Brand(models.Model):
    """Brand for clothes"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(models.Model):
    """Category for clothes"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class SubCategory(models.Model):
    """SubCategory for a category"""
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
            Category,
            related_name='subcategories',
            on_delete=models.CASCADE
        )

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return f'{self.category} - {self.name}'


class Shop(models.Model):
    """Shop for clothes"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=False, unique=True)
    url = models.URLField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Clothes(models.Model):
    """Cloths objects"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='clothes_owned',
        on_delete=models.PROTECT
    )
    name = models.CharField(max_length=255)
    price = models.IntegerField(blank=True)
    description = models.TextField(blank=True)
    purchased = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    images = models.ImageField(null=True, blank=True,
                               upload_to=clothes_image_file_path)
    brand = models.ForeignKey(
         Brand,
         related_name='brand_clothes',
         on_delete=models.PROTECT
    )
    tags = models.ManyToManyField(
         Tag,
         related_name='tag_clothes',
    )
    shop = models.ForeignKey(
        Shop,
        related_name='shop_clothes',
        on_delete=models.PROTECT,
    )
    sub_category = models.ForeignKey(
        SubCategory,
        related_name='cloth_subcategory',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name
