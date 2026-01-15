from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from locations.models import Locations

# Create your models here.


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name='feedbacks')
    comments = models.TextField()
    comments_like = models.BooleanField(default=False)
    comments_dislike = models.BooleanField(default=False)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-created_at']
        unique_together = ['user', 'location']  # Prevent duplicate feedbacks from same user

    def __str__(self):
        return f"{self.user.username} - {self.location.name} ({self.stars} stars)"
