from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Comic)
admin.site.register(NewsFeed)
admin.site.register(Character)
admin.site.register(Creator)

