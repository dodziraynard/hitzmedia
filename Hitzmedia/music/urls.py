from django.conf.urls import include
from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [    
    path('', views.index, name='index'),

    path('register/', views.register, name='register'),

    path('login_user/', views.login_user, name='login_user'),

    path('logout_user/', views.logout_user, name='logout_user'),

    path('music/<int:album_id>/', views.detail, name='detail'),

    path('music/<int:song_id>/favorite/', views.favorite, name='favorite'),

    path('music/songs/<filter_by>/', views.songs, name='songs'),

    path('music/create_album/', views.create_album, name='create_album'),

    path('music/album/<int:pk>/', views.AlbumUpdate.as_view(), name='update_album'),

    path('music/<int:album_id>/create_song/', views.create_song, name='create_song'),

    path('music/delete_comment/<int:comment_id>/<int:album_id>/', views.delete_comment, name='delete_comment'),

    path('music/<int:album_id>/delete_song/<int:song_id>/', views.delete_song, name='delete_song'),    

    path('music/<int:album_id>/favorite_album/', views.favorite_album, name='favorite_album'),

    path('music/<int:album_id>/delete_album/', views.delete_album, name='delete_album'),

    path('music/email/', views.email, name='email'),
]
