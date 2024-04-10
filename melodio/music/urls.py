from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('allsongs',views.allsongs,name='allsongs'),
    path('song/<int:song_id>/', views.eachsong, name='eachsong'),
    path('genres',views.genres,name='genres'),
    path('genre/<int:genre_id>/', views.genre_songs, name='genre_songs'),
    path('artists/', views.artists, name='artists'),
    path('artist/<int:artist_id>/', views.artist_songs, name='artist_songs'),
    path('albums/', views.all_albums, name='all_albums'),
    path('albums/<int:album_id>/', views.album_songs, name='album_songs'),
    path('watchlater', views.watchlater, name='watchlater'),
    path('remove_from_watchlater', views.watchlater, name='remove_from_watchlater'),
    path('search', views.search, name='search'),
    path('uploadsong/', views.upload_song, name='uploadsong'),
]
