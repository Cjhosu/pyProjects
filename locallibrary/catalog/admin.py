from django.contrib import admin

# Register your models here.
from .models import Book, Item, Comic, Item_type, Item_status

admin.site.register(Book)
admin.site.register(Item)
admin.site.register(Comic)
admin.site.register(Item_type)
admin.site.register(Item_status)
