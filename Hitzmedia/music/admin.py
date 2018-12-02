from django.contrib import admin
from .models import Album, Song, Comment, Email

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Comment)
admin.site.register(Email)