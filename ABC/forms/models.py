from django.db import models

# Create your models here.


class FormExample(models.Model):
    image_url = models.URLField(blank=True)
    url = models.URLField(blank=True)
    html = models.TextField(blank=True)
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)

