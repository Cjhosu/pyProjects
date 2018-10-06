from django.contrib import admin

# Register your models here.
from .models import Book, Item, Item_request, Comic, Item_type, Item_status

admin.site.register(Book)
admin.site.register(Item)
admin.site.register(Comic)
admin.site.register(Item_type)
admin.site.register(Item_request)
class Item_statusAdmin(admin.ModelAdmin):
    list_display = ('itemname', 'borrower','id')
    list_filter = ('id','borrower')
    fieldset = (
        (None, {
            'fields': ('id', 'borrower')
        })
    )
admin.site.register(Item_status, Item_statusAdmin)
