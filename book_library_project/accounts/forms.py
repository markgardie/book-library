from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'birth_date', 'favorite_genre']
        labels = {
            'bio': 'Біографія',
            'avatar': 'Аватар',
            'birth_date': 'Дата народження',
            'favorite_genre': 'Улюблений жанр',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'favorite_genre': forms.TextInput(attrs={'class': 'form-control'}),
        }