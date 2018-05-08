from django.contrib import admin

# Register your models here.
from .models import Comic, NewsFeed

admin.site.register(Comic)
admin.site.register(NewsFeed)