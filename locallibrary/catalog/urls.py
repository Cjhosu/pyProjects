from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'comics/$', views.ComicListView.as_view(), name = 'comics'),
    url(r'^books/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='books-detail'),
]
