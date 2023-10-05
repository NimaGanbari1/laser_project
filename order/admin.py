# Django
from django.contrib import admin

# Local
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'ProductCodes', 'ProductCounts', 'Price',
                    'user', 'status_pay', 'consumed_code', 'create_time']
    date_hierarchy = 'create_time'
    list_filter = ['create_time', 'Price']
    readonly_fields = ('ProductCodes', 'ProductCounts', 'Price',
                       'consumed_code', 'user', 'create_time', 'Address', 'status_pay')


admin.site.register(Order, OrderAdmin)
