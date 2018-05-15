from django.shortcuts import render
from django.views.generic import ListView
from notifications.models import Notification

# Create your views here.
class NotificationList(ListView):
    model = Notification
    template_name = 'notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self, request):
        return Notification.objects.filter(user=request.user).order_by('-created_at')
