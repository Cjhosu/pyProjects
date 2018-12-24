from ..forms import AddBookForm, UpdateBookForm
from ..models import Book, Item, Item_request, Item_status, Item_type
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.views import generic, View
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect


class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    paginate_by = 10
    ordering = ('title', )

    def get_queryset(self,**kwargs):
        filter_val = self.request.GET.get('search', '')
        return Book.objects.filter(Q(title__icontains = filter_val) | Q(author_last__icontains = filter_val)).order_by('title')


class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book

class BookUpdateView(LoginRequiredMixin,View):
    model = Book

    def get(self, request, pk):
        bkinstance = get_object_or_404(Book, pk=pk)
        form = UpdateBookForm(instance=bkinstance)
        return render(request, 'catalog/book_form.html', {'form': form})

    def post(self, request, pk):
        bkinstance = get_object_or_404(Book, pk=pk)
        form = UpdateBookForm(request.POST , instance=bkinstance)
        if form.is_valid():
            form.save()
            return redirect('/catalog/books/')

def AddItem(request, form, type_id):
    if request.POST:
        additem = Item()
        additem.item_name = form.cleaned_data['item_name']
        additem.item_type_id = type_id
        additem.owned_by = request.user
        additem.added_at = datetime.now()
        additem.updated_at = datetime.now()
        additem.save()
        return additem.id

def AddNewBook(request):
    if request.POST:
        form = AddBookForm(request.POST)
        item_type = Item_type.objects.get(type = 'Book')
        type_id = item_type.id
        if form.is_valid():
            obj_id = AddItem(request, form, type_id)
            addbook = Book()
            addbook.item_id = obj_id
            addbook.title = form.cleaned_data['title']
            addbook.author_first = form.cleaned_data['author_first']
            addbook.author_last = form.cleaned_data['author_last']
            addbook.isbn = form.cleaned_data['isbn']
            addbook.publisher = form.cleaned_data['publisher']
            addbook.year = form.cleaned_data['year']
            addbook.description  = form.cleaned_data['description']
            addbook.save()

            addstatus = Item_status()
            addstatus.item_id = obj_id

            addstatus.save()

            return HttpResponseRedirect('/catalog/books/')
    else:
        form = AddBookForm()
    return render(request, 'catalog/add_book_form.html', {'form': form})

def IssueBookRequest(request,pk):
    bookreq = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        bookitem = Book.objects.get(pk=pk)
        obj, created = Item_request.objects.update_or_create(
            item_id = bookitem.item_id,
            requester = request.user,
            filled_at = None,
          defaults = {'is_accepted':None, 'requested_at': datetime.now()}
        )
        messages.info(request, 'Your request has been received!')
        return HttpResponseRedirect('/catalog/books/'+pk)
    else:
        return HttpResponseRedirect('/catalog/')

