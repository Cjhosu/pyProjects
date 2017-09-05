from django.shortcuts import render

# Create your views here.
from .models import Item, Item_type, Book, Comic, Item_status
from django.views import generic

def index(request):
    num_books=Book.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_books':num_books},
)

class BookListView(generic.ListView):
    model = Book

class ComicListView(generic.ListView):
    model = Comic
