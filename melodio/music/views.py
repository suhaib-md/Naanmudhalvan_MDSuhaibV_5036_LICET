from django.shortcuts import render, redirect
from django.db.models import Case, When
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import * 
from . form import *

# Create your views here.
def home(request):
    albums = Album.objects.all()
    artists = Artist.objects.all()
    genres = Genre.objects.all()
    existing_songs = Song.objects.select_related('album').all()
    uploaded_songs = UploadedSong.objects.all()
    # Combine the two querysets
    all_songs = list(existing_songs) + list(uploaded_songs)
    return render(request,'music/index.html',{'albums': albums, 'artists': artists, 'genres': genres,"all_songs": all_songs})

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Hash the user's password before saving
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Registeration successfull")
            return redirect('/login')
    return render(request,'music/register.html',{'form':form})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully")
    return redirect('/') 

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/') 
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('/login')
        return render(request,'music/login.html')

def allsongs(request):
    existing_songs = Song.objects.select_related('album').all()
    uploaded_songs = UploadedSong.objects.all()
    # Combine the two querysets
    all_songs = list(existing_songs) + list(uploaded_songs)
    return render(request,'music/allsongs.html', {'all_songs':all_songs} )

def genres(request):
    genres = Genre.objects.all()
    return render(request, 'music/genres.html', {'genres': genres})

def genre_songs(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    songs = Song.objects.filter(genres=genre)
    return render(request, 'music/genre_songs.html', {'genre': genre, 'songs': songs})

def artists(request):
    artists = Artist.objects.all()
    return render(request, 'music/artists.html', {'artists': artists})

def artist_songs(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    songs = Song.objects.filter(album__artist=artist)
    return render(request, 'music/artist_songs.html', {'artist': artist, 'songs': songs})

def all_albums(request):
    albums = Album.objects.all()
    return render(request, 'music/albums.html', {'albums': albums})

def album_songs(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/album_songs.html', {'album': album})

def eachsong(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    return render(request, 'music/eachsong.html', {'song': song})

def watchlater(request):
    if request.method == 'POST':
        # Check if the request is for adding or removing from watch later
        if 'song_id' in request.POST:
            user = request.user
            song_id = request.POST['song_id']
            watch = WatchLater.objects.filter(user=user)
            for i in watch:
                if song_id == i.songs_id:
                    messages.error(request, 'Song already exists')
                    return redirect('/allsongs')
            else:
                watchlater = WatchLater(user=user, songs_id=song_id)
                watchlater.save()
                messages.success(request, "Added to listen later")
                return redirect('/allsongs')
        elif 'remove_song_id' in request.POST:
            user = request.user
            song_id = request.POST['remove_song_id']
            try:
                watchlater = WatchLater.objects.get(user=user, songs_id=song_id)
                watchlater.delete()
                messages.success(request, "Removed from listen later")
            except WatchLater.DoesNotExist:
                messages.error(request, 'Song not found in listen later list')

    wl = WatchLater.objects.filter(user=request.user)
    ids = list(wl.values_list('songs_id', flat=True))
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    all_songs = Song.objects.filter(id__in=ids).order_by(preserved)
    return render(request, 'music/watchlater.html', {"all_songs": all_songs})

def search(request):
    query = request.GET.get('query')
    song = Song.objects.all()
    qs = song.filter(title__icontains=query)
    
    return render(request, 'music/search.html', {"songs": qs})

def upload_song(request):
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_song = form.save(commit=False)
            uploaded_song.uploaded_by = request.user  # Set the uploaded_by field to the current user
            uploaded_song.save()
            messages.success(request,"Song Uploaded Successfully")
            return redirect('/')  # Replace 'upload_success' with the URL name of the success page
    else:
        form = SongUploadForm()
    return render(request, 'music/uploadsong.html', {'form': form})