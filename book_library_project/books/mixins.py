from django.shortcuts import redirect
from django.contrib import messages

class BookOwnerMixin:
    """Mixin для перевірки власника книги"""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.added_by != request.user:
            messages.error(request, 'Ви можете редагувати тільки свої книги.')
            return redirect('library:book_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

class ReviewOwnerMixin:
    """Mixin для перевірки власника рецензії"""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            messages.error(request, 'Ви можете редагувати тільки свої рецензії.')
            return redirect('library:review_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)