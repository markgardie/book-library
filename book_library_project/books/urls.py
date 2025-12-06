from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Книги
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/add/', views.BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    
    # Рецензії
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('review/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('book/<int:book_pk>/review/add/', views.ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
]