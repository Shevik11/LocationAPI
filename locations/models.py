from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


# Create your models here.
class Locations(models.Model):
    name = models.CharField(max_length=100, unique=True)
    average_rating = models.FloatField(default=0)
    category = models.CharField(max_length=100, default="404")

    def __str__(self):
        return self.name
