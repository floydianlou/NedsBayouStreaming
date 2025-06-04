from django.contrib import admin

from .forms import ArtistAdminForm
from .models import Genre, Artist, Song, Playlist

admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Song)

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')

class ArtistAdmin(admin.ModelAdmin):
    form = ArtistAdminForm