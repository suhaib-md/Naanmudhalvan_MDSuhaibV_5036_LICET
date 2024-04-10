from django.contrib import admin
from .models import *

admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(WatchLater)
admin.site.register(UploadedSong)


