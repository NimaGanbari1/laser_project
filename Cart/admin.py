# Django
from django.contrib import admin

# Local
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'Code', 'Count', 'user']
    list_display_links = ['user', 'id']
    readonly_fields = ('Code', 'Count', 'user')
    date_hierarchy = 'create_time'


admin.site.register(Cart, CartAdmin)
