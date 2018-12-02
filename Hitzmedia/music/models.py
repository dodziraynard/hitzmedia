from django.contrib.auth.models import Permission, User
from django.db import models


class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist

class Comment(models.Model):
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.album.album_title + ' --- ' + self.comment

class Email(models.Model):
    message = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    sender = models.CharField(max_length = 100, blank=True)

    def __str__(self):
        return self.message + ' Sender: ' + self.sender + '  Contact: ' + self.contact
    

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
