from django.dispatch import receiver
from app.signals import notifications
from notifications.models import Notification

@receiver(notifications)
def add_notifications(sender, **kwargs):
    print(sender)
    n = Notification.objects.create(user=kwargs['user'], message=kwargs['message'], link=kwargs['link'])
    n.save()
