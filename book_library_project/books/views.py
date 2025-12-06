from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Book, Review
from .forms import BookForm, ReviewForm
from .mixins import BookOwnerMixin, ReviewOwnerMixin

class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Book.objects.all()
        search_query = self.request.GET.get('search')
        genre_filter = self.request.GET.get('genre')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if genre_filter:
            queryset = queryset.filter(genre=genre_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Book.objects.values_list('genre', flat=True).distinct()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_genre'] = self.request.GET.get('genre', '')
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['reviews'] = book.reviews.all()
        context['user_review'] = None
        
        if self.request.user.is_authenticated:
            try:
                context['user_review'] = Review.objects.get(book=book, user=self.request.user)
            except Review.DoesNotExist:
                pass
                
        return context

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_create.html'
    
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        messages.success(self.request, 'Книга успішно додана!')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, BookOwnerMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_update.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Книга успішно оновлена!')
        return super().form_valid(form)

class BookDeleteView(LoginRequiredMixin, BookOwnerMixin, DeleteView):
    model = Book
    template_name = 'library/book_delete.html'
    success_url = reverse_lazy('library:book_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Книга успішно видалена!')
        return super().delete(request, *args, **kwargs)

class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'library/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'library/review_detail.html'
    context_object_name = 'review'

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'library/review_create.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs['book_pk'])
        # Перевіряємо, чи користувач вже не залишив рецензію на цю книгу
        if Review.objects.filter(book=self.book, user=request.user).exists():
            messages.error(request, 'Ви вже залишили рецензію на цю книгу.')
            return redirect('library:book_detail', pk=self.book.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = self.book
        messages.success(self.request, 'Рецензія успішно додана!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context

class ReviewUpdateView(LoginRequiredMixin, ReviewOwnerMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'library/review_update.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Рецензія успішно оновлена!')
        return super().form_valid(form)

class ReviewDeleteView(LoginRequiredMixin, ReviewOwnerMixin, DeleteView):
    model = Review
    template_name = 'library/review_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('library:book_detail', kwargs={'pk': self.object.book.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Рецензія успішно видалена!')
        return super().delete(request, *args, **kwargs)