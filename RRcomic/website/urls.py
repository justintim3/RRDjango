from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('comicpage', views.get_comic_page, name = 'comicpage'),
    path('comic', views.get_comic, name = 'comic'),
    path('ajax/verifyUser', views.verify_user, name='verify_user'),
    path('ajax/dosignup', views.create_user, name='create_user')
]
