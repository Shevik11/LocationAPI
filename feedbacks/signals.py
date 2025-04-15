from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Feedback
from users.models import User
from django.core.mail import send_mail


@receiver(post_save, sender=Feedback)
def feedback_created(sender, instance, created, **kwargs):
    if created:
        subscibed_user = User.objects.filter(subscription=True)
        for user in subscibed_user:
            send_mail(
                "New feedback added",
                f"New feedback has been addded to: {instance.location}",
                "maxname904496@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
        print(f"Feedback created: {instance}")
