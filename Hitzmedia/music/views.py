from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm, CommentForm, EmailForm
from .models import Album, Song, Comment

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_album(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)

def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.all()
    return render(request, 'music/index.html', {'albums': albums})

def delete_comment(request, comment_id, album_id):
    comment = Comment.objects.get(pk=comment_id)    
    album = Album.objects.get(pk=album_id)
    comment.delete()
    return render(request, 'music/detail.html', {'album': album})

def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})


def detail(request, album_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        album = get_object_or_404(Album, pk=album_id)
        comment.album = album
        comment.user = request.user        
        comment.comment = form.cleaned_data['comment']
        comment.save()

    if not request.user.is_authenticated:
        user = None
    else:
        # Album user (owner)
        user = request.user
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album, 'user': user, 'form':form})

def email(request):
    form = EmailForm(request.POST or None)
    if form.is_valid():
        email = form.save(commit=False)
        email.message = form.cleaned_data['message']
        email.sender = request.user.username        
        email.contact = form.cleaned_data['contact']
        email.save()
        albums = Album.objects.all()
        context = {
                'albums': albums, 
                'user': request.user,
                'form': form,
                'email_sent': 'E-mail successfully sent',
        }
        return render(request, 'music/index.html', context)
    return render(request, 'music/index.html', {'error': form.errors})

def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def index(request):
    if not request.user.is_authenticated:
        user = None
    else:
        user = request.user        
    albums = Album.objects.all()    
    song_results = Song.objects.all()
    query = request.GET.get("q")

    if not query:
        return render(request, 'music/index.html', {'albums': albums, 'user': user})


    if query:
        albums = albums.filter(
            Q(album_title__icontains=query) |
            Q(artist__icontains=query)
        ).distinct()
        song_results = song_results.filter(
            Q(song_title__icontains=query)
        ).distinct()
        return render(request, 'music/index.html', {
            'albums': albums,
            'songs': song_results,
            'user': user,
        })
    else:
        return render(request, 'music/index.html', {'albums': albums, 'user': user})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums, 'user': request.user})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
            'user': request.user
        })

class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']
    success_url = reverse_lazy('music:index')

class CommentDelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('music:index')