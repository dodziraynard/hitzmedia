from django import forms
from django.contrib.auth.models import User

from .models import Album, Song, Comment, Email


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['comment']

class EmailForm(forms.ModelForm):
    
    class Meta:
        model = Email
        fields = ['message', 'contact', 'sender']

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
