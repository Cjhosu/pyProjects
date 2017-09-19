from django.conf.urls import url
from .forms import AddBookForm
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'comics/$', views.ComicListView.as_view(), name = 'comics'),
    url(r'^books/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='books-detail'),
    url(r'^mybooks/$', views.LoanedItemsByUserListView.as_view(), name='my-books'),
    url(r'^books/add/$', views.AddNewBook, name='add_book'),
    url(r'^add_item/$', views.AddNewItem, name='add_item'),
    url(r'mark-returned/(?P<pk>\d+)$',views.MarkReturned, name='mark-returned'),
]
