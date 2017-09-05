from django.db import models
import datetime
from django.utils import timezone
# Create your models here.


class Item_type(models.Model):
    type = models.CharField(max_length=50)
    def __str__(self):
      return self.type

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_type = models.ForeignKey(Item_type, on_delete=models.SET_NULL, null=True)
    owned_by = models.CharField(max_length=255)
    added_at = models.DateTimeField('date item added')
    updated_at = models.DateTimeField('last update')
    def __str__(self):
      return self.item_name

class Book(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    author_first = models.CharField(max_length=100)
    author_last = models.CharField(max_length=100)
    isbn = models.CharField(max_length=15)
    publisher = models.CharField(max_length=30)
    year = models.CharField(max_length=4)
    def __str__(self):
      return self.title

class Comic(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    publisher = models.CharField(max_length=30)
    series = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    number = models.IntegerField(default=None, blank=True, null=True)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=3)
    def __str__(self):
      return (self.series)

class Item_status(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    loaned_to = models.IntegerField(default=None, blank=True, null=True)
    loaned_at = models.DateTimeField(default=None, blank=True, null=True)
    due_back = models.DateTimeField(default=None, blank=True, null=True)
    def __str__(self):
     return self.loaned_at



