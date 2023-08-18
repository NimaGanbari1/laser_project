from django.contrib import admin
#from django.contrib.auth.models import Permission,Group
from .models import Order


#class OrderChangePermission(Permission):
#    name = "Can change order details"
#    content_type = Order.objects.get_for_model(Order)
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','ProductCodes','ProductCounts','Price','user','status_pay','consumed_code','create_time']
    #def list_of_amenities(self, obj):
    #    return ([Category.title for category in obj.categories.all()])
    #list_of_amenities.short_description = 'Category'
    #list_editable = ['status']
    #list_display_links = ['title','price']
    #list_per_page = 5
    #date_hierarchy = 'create_time'
    #search_fields = ['title','uniqe_code','is_enable']
    #list_filter = ['create_time']
    #filter_horizontal = ['categories']
    #search_fields = ['title']
    #inlines = [CommentInLineAdmin,PostInLineAdmin]
    #empty_value_display = 'Unknown Item field'
    #def has_add_permission(self, request,obj=None):
    #    return False
    #def has_change_permission(self, request,obj=None):
    #    return False
    def has_delete_permission(self, request,obj=None):
        return False
    readonly_fields = ('ProductCodes','ProductCounts','Price','consumed_code','user','create_time','Address','status_pay')


#admin_group = Group.objects.get(name='admin')
#order_change_permission = Permission.objects.get(name='Can change order details')
#admin_group.permissions.add(order_change_permission)

admin.site.register(Order,OrderAdmin)
#admin.site.register(OrderChangePermission)
# Register your models here.
