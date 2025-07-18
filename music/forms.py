from PIL import Image
from django import forms
from django.core.exceptions import ValidationError
from .models import *


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'cover', 'songs']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Playlist name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Caption'
            }),
            'songs': forms.CheckboxSelectMultiple()
        }

    def clean_cover(self):
        image = self.cleaned_data.get('cover')
        if image:
            try:
                img = Image.open(image)
                img.verify()
            except Exception:
                raise ValidationError("Please upload a valid image file.")
        return image


# error does not make update form unusable, it just does not recognize the queryset
class PlaylistUpdateForm(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Songs in playlist"
    )

    class Meta:
        model = Playlist
        fields = ['name', 'description', 'cover', 'songs']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Playlist name'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Caption'}),
            'cover': forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['songs'].queryset = Song.objects.all()
        if self.instance:
            self.fields['songs'].initial = self.instance.songs.all()

    def clean_cover(self):
        image = self.cleaned_data.get('cover')
        if image:
            try:
                img = Image.open(image)
                img.verify()
            except Exception:
                raise ValidationError("Please upload a valid image file.")
        return image


class ArtistAdminForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'

    def clean_genres(self):
        genres = self.cleaned_data.get('genres')
        if genres.count() < 1:
            raise forms.ValidationError("Please select at least one genre")
        if genres.count() > 3:
            raise forms.ValidationError("The maximum genres allowed is 3.")
        return genres

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            try:
                img = Image.open(photo)
                img.verify()
            except Exception:
                raise ValidationError("Please upload a valid image file.")
        return photo

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Genre name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Genre description'}),
        }

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Song title'}),
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'audio_file': forms.ClearableFileInput(),
            'cover': forms.ClearableFileInput(),
        }

    def clean_audio_file(self):
        file = self.cleaned_data.get('audio_file')

        if not file:
            raise forms.ValidationError("You can't submit a song without an audio file.")
        if not hasattr(file, 'content_type') or not file.content_type.startswith('audio'):
            raise forms.ValidationError("You can't submit a song without an audio file.")

        if file.size > 20 * 1024 * 1024:
            raise forms.ValidationError("File is too big (max 20MB).")
        return file

    def clean_cover(self):
        image = self.cleaned_data.get('cover')
        if image:
            try:
                img = Image.open(image)
                img.verify()
            except Exception:
                raise ValidationError("Please upload a valid image file.")
        return image