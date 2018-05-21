from django.urls import path
from django.conf.urls import include
from django import urls
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('comicpage', views.get_comicpage, name = 'comicpage'),
    path('characterpage', views.get_characterpage, name = 'characterpage'),
    path('newsfeedpage', views.get_newsfeedpage, name = 'newsfeedpage'),
    path('creatorpage', views.get_creatorpage, name = 'creatorpage'),
    path('comic', views.get_comic, name = 'comic'),
    path('character', views.get_character, name = 'character'),
    path('creator', views.get_creator, name = 'creator'),
    path('profile', views.get_profile, name='profile'),
    path('signup',views.signup, name = 'signup'),
    path('about', views.get_about, name = 'about'),
    path('newsfeed', views.get_newsfeed, name = 'newsfeed'),
    path('publisherpage', views.get_publisherpage, name = 'publisherpage'),
    path('seriespage', views.get_seriespage, name = 'seriespage')

    #url(r'^login/$', auth_views.login)
    #path('accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    #static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
]
