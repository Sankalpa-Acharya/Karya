from dataclasses import field
from django import forms
from .models import Project, User,Card
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=  '__all__'



class SingupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class ProfileEditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','email','bio','twitter','github','linkedin']

class ProfilePictureChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['profile_pic']


class CardStatusChangeForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['status']

class AddCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['title','description'] 


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description']