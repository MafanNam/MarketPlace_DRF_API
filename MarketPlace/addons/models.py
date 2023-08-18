import os

from django.db import models
from datetime import date


def get_upload_path_main_news(instance, filename):
    now_data = date.today()
    return os.path.join(
        "Addons", "News", now_data.strftime('%Y'),
        now_data.strftime('%m'), filename)


class News(models.Model):
    """News model."""
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_upload_path_main_news, blank=True)
    text = models.TextField(max_length=1000, blank=True)

    # additional fields
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'News'


class Main(models.Model):
    name = models.CharField(max_length=255)
    text = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Main'


class About(models.Model):
    name = models.CharField(max_length=255)
    text = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class Licence(models.Model):
    name = models.CharField(max_length=255)
    text = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Licence'
