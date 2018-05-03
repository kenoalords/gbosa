"""gbosa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from app.views import SearchList, PostList, SocialLoginView, account_logout, PsuedoCreate, UserPostList

urlpatterns = [
    path('', PostList.as_view(), name="index"),
    url(r'^sw(.*.js)$', TemplateView.as_view(template_name="sw.js", content_type="application/x-javascript"), name="sw"),
    path('post/', include('app.urls')),
    path('search/', SearchList.as_view(), name="search"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login/', SocialLoginView.as_view(), name="social-login"),
    path('logout/', account_logout, name="logout"),
    path('psuedonym/', PsuedoCreate.as_view(), name='psuedonym'),
    path('my-posts/', UserPostList.as_view(), name='user-posts')
]
