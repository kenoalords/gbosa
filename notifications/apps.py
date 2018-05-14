from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    name = 'notifications'
    def ready(self):
        from app.signals import notifications
        from app.models import Comment
        from notifications.receivers import add_notifications

        notifications.connect(add_notifications)
