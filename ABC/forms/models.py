from django.db import models

# Create your models here.


class FormExample(models.Model):
    image_url = models.URLField(blank=False)
    url = models.URLField()

