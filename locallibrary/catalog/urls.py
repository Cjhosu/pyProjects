from django.conf.urls import url
from .forms import AddBookForm
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'comics/$', views.ComicListView.as_view(), name = 'comics'),
    url(r'^books/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='books-detail'),
    url(r'^books/(?P<pk>\d+)/update/$', views.BookUpdateView.as_view(), name='book_update'),
    url(r'^comics/(?P<pk>\d+)$', views.ComicDetailView.as_view(), name='comics-detail'),
    url(r'^comics/(?P<pk>\d+)/update/$', views.ComicUpdateView.as_view(), name='comic_update'),
    url(r'^mybooks/$', views.LoanedItemsByUserListView.as_view(), name='my-books'),
    url(r'^books/add/$', views.AddNewBook, name='add_book'),
    url(r'^comics/add/$', views.AddNewComic, name='add_comic'),
    url(r'^add_item/$', views.AddNewItem, name='add_item'),
    url(r'^cust_mes/(?P<pk>\d+)$',views.CustMes, name='cust_mes'),
    url(r'mark-returned/(?P<pk>\d+)$',views.MarkReturned, name='mark-returned'),
    url(r'accept-request/(?P<pk>\d+)$',views.AcceptRequest, name='accept-request'),
    url(r'ack-message/(?P<pk>\d+)$',views.AckMessage, name='ack-message'),
    url(r'^loan_item/$', views.LoanItem, name='loan_item'),
    url(r'^convert_user/(?P<pk>\d+)$', views.ConvertInactiveUser, name='convert_user'),
    url(r'^inactive_user/$', views.CreateInactiveUser, name='incative_user'),
    url(r'pass-borrower/(?P<pk>\d+)$',views.PassBorrower, name='pass-borrower'),
    url(r'issue-book-request/(?P<pk>\d+)$',views.IssueBookRequest, name='issue-book-request'),
    url(r'issue-comic-request/(?P<pk>\d+)$',views.IssueComicRequest, name='issue-comic-request'),
    url(r'^signup/$',views.signup, name='signup'),
    url(r'^user_alerts/$', views.UserAlertView, name='user-alerts'),
]
