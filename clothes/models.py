from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


class Tag(models.Model):
    """Tag to be used for clothes"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
