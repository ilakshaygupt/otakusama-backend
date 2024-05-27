from django.contrib import admin

from UserData.models import  Manga, UserProfile

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Manga)

