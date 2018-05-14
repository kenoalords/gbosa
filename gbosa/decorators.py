from django.core.exceptions import PermissionDenied
from app.models import Post

def current_user_is_owner(function):
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if ( post.user == request.user ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def post_is_not_flagged(function):
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if ( post.is_flagged == False ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def post_is_not_deleted(function):
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if ( post.is_deleted == False ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
