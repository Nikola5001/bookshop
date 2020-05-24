from django import forms
from .models import Artikl
from .models import Recenzija
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#DataFlair
class ArtiklCreate(forms.ModelForm):
    class Meta:
        model = Artikl
        fields = '__all__'

class RecenzijaCreate(forms.ModelForm):
    class Meta:
        model = Recenzija
        fields = '__all__'

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )