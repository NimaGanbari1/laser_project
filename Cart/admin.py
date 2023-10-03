from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','Code','Count','user']
    #زمانی که بر روی یوزر در پنل ادمین کلیک میکنیم ارور میدهد
    #list_display_links = ['user']
    #pass
    
admin.site.register(Cart,CartAdmin)
