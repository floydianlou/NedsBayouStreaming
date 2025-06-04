from django import forms
from .models import Playlist, Song, Artist

from django import forms

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'cover', 'songs']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome della playlist'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description (facultative)'
            }),
            'songs': forms.CheckboxSelectMultiple()
        }



class PlaylistUpdateForm(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Canzoni nella playlist"
    )

    class Meta:
        model = Playlist
        fields = ['name', 'description', 'cover', 'songs']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome della playlist'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrizione'}),
            'cover': forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['songs'].queryset = Song.objects.all()
        if self.instance:
            self.fields['songs'].initial = self.instance.songs.all()


class ArtistAdminForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'

    def clean_genres(self):
        genres = self.cleaned_data.get('genres')
        if genres.count() < 1:
            raise forms.ValidationError("Seleziona almeno un genere.")
        if genres.count() > 3:
            raise forms.ValidationError("Puoi selezionare al massimo 3 generi.")
        return genres