from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва")
    author = models.CharField(max_length=100, verbose_name="Автор")
    description = models.TextField(verbose_name="Опис")
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True, verbose_name="Обкладинка")
    publication_date = models.DateField(verbose_name="Дата публікації")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    pages = models.PositiveIntegerField(verbose_name="Кількість сторінок")
    genre = models.CharField(max_length=50, verbose_name="Жанр")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Додано користувачем")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'pk': self.pk})
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0
    
    def get_reviews_count(self):
        return self.reviews.count()

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Жахливо'),
        (2, '2 - Погано'),
        (3, '3 - Задовільно'),
        (4, '4 - Добре'),
        (5, '5 - Відмінно'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оцінка"
    )
    comment = models.TextField(verbose_name="Коментар")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    notes = models.TextField(blank=True, verbose_name="Особисті нотатки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Рецензія"
        verbose_name_plural = "Рецензії"
        unique_together = ('book', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.book.title} - {self.user.username} ({self.rating}/5)"
    
    def get_absolute_url(self):
        return reverse('library:review_detail', kwargs={'pk': self.pk})