from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from utils.ip import view_log

@shared_task
def mailer(subject, message, recipient, from_email='info@odly.com'):
    try:
        send_mail(subject, message, from_email, recipient, fail_silently=False)
    except:
        print('Could not send email')

@shared_task
def log_the_view(id, model):

    view_log(object)
