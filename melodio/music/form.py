from django.contrib.auth.forms import UserCreationForm
from .models import User, UploadedSong
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter email address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class SongUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedSong
        fields = ['title', 'artist', 'bio','album','cover_art','duration','release_date','file'] 