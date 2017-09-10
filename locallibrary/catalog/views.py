from django.shortcuts import render

# Create your views here.
from .models import Item, Item_type, Book, Comic, Item_status
from django.views import generic

def index(request):
    num_books=Book.objects.all().count()
    num_comics=Comic.objects.all().count()
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request,
        'index.html',
        context={'num_books':num_books, 'num_comics':num_comics, 'num_visits':num_visits},
)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class ComicListView(generic.ListView):
    model = Comic

class BookDetailView(generic.DetailView):
    model = Book
