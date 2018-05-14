from django.urls import path
from notifications.views import NotificationList

app_name = 'notifications'

urlpatterns = [
    path('', NotificationList.as_view(), name='index')
]
