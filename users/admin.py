from django.contrib import admin
#from .models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ('username','password')}),
        (_('personal info'),{"fields": ('first_name','last_name','phone_number','email','address')}),
        (_('permissions'),{"fields": ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        (_('important dates'),{"fields": ('last_login','date_joined')}),
        )
    
    add_fieldsets = [
        (None, {
            'classes':('wide',),
            "fields": ('username','phone_number','password1','password2')
        })
    ]

    list_display = ('id','username','phone_view','email_view','is_staff')
    search_fields = ('username__exact',)
    ordering = ('id',)
    
    #https://www.webforefront.com/django/adminreadrecords.html
    #empty_value_display = 'Unknown Item field'
    
    def email_view(self, obj):
         return obj.email
    email_view.empty_value_display = 'No known email'
    
    def phone_view(self, obj):
         return obj.phone_number
    phone_view.empty_value_display = 'No known phone'
    
    
    def get_search_results(self, request, queryset, search_term):
        queryset ,may_have_duplicates = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(phone_number =search_term_as_int)
        return queryset,may_have_duplicates


class CartAdmin(admin.ModelAdmin):
    list_display = ['id','Code','Count','user']
    #زمانی که بر روی یوزر در پنل ادمین کلیک میکنیم ارور میدهد
    #list_display_links = ['user']
    #pass
    
         
    
    
admin.site.unregister(Group)
admin.site.register(User,MyUserAdmin)  
#admin.site.register(UserProfile)  
admin.site.register(Cart,CartAdmin)