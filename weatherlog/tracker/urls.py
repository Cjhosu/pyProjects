
from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^add_location', views.AddLocation, name='add_location'),
    url(r'^create_journal', views.CreateJournal, name = 'create_journal')
]

