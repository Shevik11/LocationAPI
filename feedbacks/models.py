from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from locations.models import Locations

# Create your models here.


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    comments = models.TextField()
    comments_like = models.BooleanField(default=False)
    comments_dislike = models.BooleanField(default=False)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
