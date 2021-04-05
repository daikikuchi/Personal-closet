from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


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
