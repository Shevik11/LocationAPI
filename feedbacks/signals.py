from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Feedback
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
from locations.utils import calculate_average_rating


def update_location_rating(location):
    """Helper function to update location's average rating"""
    location.average_rating = calculate_average_rating(location.id)
    location.save()


@receiver(post_save, sender=Feedback)
def feedback_saved(sender, instance, created, **kwargs):
    """Signal to update location rating and send email notifications"""
    # Update average rating for the location
    update_location_rating(instance.location)
    
    # Send email notification to subscribed users when new feedback is created
    if created:
        subscribed_users = User.objects.filter(subscription=True).exclude(email='')
        if subscribed_users.exists() and settings.EMAIL_HOST_USER:
            try:
                recipient_list = list(subscribed_users.values_list('email', flat=True))
                send_mail(
                    subject="New feedback added",
                    message=f"New feedback has been added to: {instance.location.name}\n\n"
                           f"Rating: {instance.stars} stars\n"
                           f"Comment: {instance.comments[:100]}...",
                    from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                    recipient_list=recipient_list,
                    fail_silently=True,  # Don't raise exception if email fails
                )
            except Exception as e:
                # Log error but don't fail the feedback creation
                print(f"Error sending email notification: {e}")


@receiver(post_delete, sender=Feedback)
def feedback_deleted(sender, instance, **kwargs):
    """Signal to update location rating when feedback is deleted"""
    update_location_rating(instance.location)
