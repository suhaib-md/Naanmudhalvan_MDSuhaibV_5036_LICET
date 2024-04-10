from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='genres/', blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', blank=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name

class Album(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField(null=True, default=None)
    cover_art = models.ImageField(upload_to='albums/', blank=True, null=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file = models.FileField(upload_to='songs/')
    duration = models.PositiveIntegerField()  # Duration of the song in seconds
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

class WatchLater(models.Model):
    listen_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs_id = models.CharField(max_length=10000000,default="")
    
class UploadedSong(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    album = models.CharField(max_length=100)
    cover_art = models.ImageField(upload_to='albums/', blank=True)
    duration = models.PositiveIntegerField()
    release_date = models.DateField()
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Check if the artist exists, if not create a new artist
        artist, _ = Artist.objects.get_or_create(name=self.artist, defaults={'bio': self.bio})
         #Check if the album exists, if not create a new album
        album, _ = Album.objects.get_or_create(title=self.album, artist=artist)
        self.artist = artist
        self.album = album
        super().save(*args, **kwargs)
    



