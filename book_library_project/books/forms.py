from django import forms
from .models import Book, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'cover', 'publication_date', 
                 'isbn', 'pages', 'genre']
        labels = {
            'title': 'Назва книги',
            'author': 'Автор',
            'description': 'Опис',
            'cover': 'Обкладинка',
            'publication_date': 'Дата публікації',
            'isbn': 'ISBN',
            'pages': 'Кількість сторінок',
            'genre': 'Жанр',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cover': forms.FileInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'is_read', 'notes']
        labels = {
            'rating': 'Оцінка',
            'comment': 'Коментар',
            'is_read': 'Прочитано',
            'notes': 'Особисті нотатки',
        }
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }