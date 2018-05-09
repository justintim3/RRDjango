from django.urls import path
from django.conf.urls import include
from django import urls
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('comicpage', views.get_comic_page, name = 'comicpage'),
    path('comic', views.get_comic, name = 'comic'),
    path('ajax/verifyUser', views.verify_user, name='verify_user'),
    path('ajax/dosignup', views.create_user, name='create_user'),
    path('profile', views.get_profile, name='profile'),
    path('signup', views.get_signuppage, name='signup'),
    #url(r'^login/$', auth_views.login)
    #path('accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

