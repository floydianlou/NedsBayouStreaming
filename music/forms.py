from django import forms
from .models import Playlist, Song

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