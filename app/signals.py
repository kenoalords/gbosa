import django.dispatch
notifications = django.dispatch.Signal(providing_args=['user','message', 'link'])
