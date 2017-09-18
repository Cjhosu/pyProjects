from django.shortcuts import render
from .forms import AddBookForm
from .forms import AddItemForm
from django.http import HttpResponseRedirect
from datetime import datetime
# Create your views here.
from .models import Item, Item_type, Book, Comic, Item_status
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F


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


class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    paginate_by = 10


class ComicListView(LoginRequiredMixin,generic.ListView):
    model = Comic


class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book


class LoanedItemsByUserListView(LoginRequiredMixin,generic.ListView):
    model = Item_status
    template_name ='catalog/item_status_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Item_status.objects.filter(borrower=self.request.user).order_by('due_back')

    def get_context_data(self, **kwargs):
        context = super(LoanedItemsByUserListView, self).get_context_data(**kwargs)
        context['Owned_list'] = Item.objects.filter(owned_by=self.request.user, item_type = 1)
        context['Loaned_list'] = Item_status.objects.filter(item__owned_by=self.request.user).exclude(borrower=self.request.user).exclude(borrower__isnull=True)
        context['Other_list'] = Item_status.objects.filter(item__owned_by=self.request.user).exclude(borrower=self.request.user).filter(borrower__isnull=True)
        return context


def AddNewBook(request):
    if request.POST:
        form = AddBookForm(request.POST)
        if form.is_valid():
            additem= Item ()
            additem.item_name = form.cleaned_data['item_name']
            additem.item_type_id = 1
            additem.owned_by = request.user
            additem.added_at = datetime.now()
            additem.updated_at = datetime.now()
            additem.save()

            obj_id = additem.id

            addbook = Book()
            addbook.item_id = additem.id
            addbook.title = form.cleaned_data['title']
            addbook.author_first = form.cleaned_data['author_first']
            addbook.author_last = form.cleaned_data['author_last']
            addbook.isbn = form.cleaned_data['isbn']
            addbook.publisher = form.cleaned_data['publisher']
            addbook.year = form.cleaned_data['year']
            addbook.description  = form.cleaned_data['description']
            addbook.save()

            addstatus = Item_status()
            addstatus.item_id = additem.id

            addstatus.save()

            return HttpResponseRedirect('/catalog/books/')
    else:
        form = AddBookForm()
    return render(request, 'catalog/add_book_form.html', {'form': form})


def AddNewItem(request):
    if request.POST:
        form = AddItemForm(request.POST)
        if form.is_valid():
#            if request.POST = 'Book'
            return HttpResponseRedirect(request,render,'/catalog/add_book_form.html')
    else:
        form = AddItemForm()
        return render(request, 'catalog/add_item.html', {'form':form})

