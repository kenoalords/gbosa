from utils.ip import get_tags
from notifications.models import Notification

def tags_context_processor(request):
    return { 'tags': get_tags() }

def unread_notifications(request):
    return { 'unread_notifications': Notification.objects.filter(user=request.user, is_viewed=False).count() }
