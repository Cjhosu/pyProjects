import django_filters
from .models import Book, Comic

class BookListFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ['title' , 'author_last']
        order_by = ['title']

