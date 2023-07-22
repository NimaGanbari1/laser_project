from django.contrib import admin
from .models import Category , Product, Comment , Post_File
#admin.site.empty_value_display = '???'

class CommentInLineAdmin(admin.TabularInline):
    model = Comment
    #user add in fields
    fields = ['id','text']
    extra = 0

class PostInLineAdmin(admin.TabularInline):
    model = Post_File
    #user add in fields
    fields = ['id','title','file_type','fil','is_enable']
    readonly_fields=['create_time']
    extra = 0

class PostFileAdmin(admin.ModelAdmin):
    list_display = ['id','title','uniqe_code','price','create_time','is_enable','list_of_amenities','is_active']
    def list_of_amenities(self, obj):
        return ([Category.title for category in obj.categories.all()])
    list_of_amenities.short_description = 'Category'
    #list_editable = ['title','price','is_enable']
    #list_display_links = ['title','price']
    list_per_page = 5
    date_hierarchy = 'create_time'
    search_fields = ['title','uniqe_code','is_enable']
    #list_filter = ['create_time']
    filter_horizontal = ['categories']
    search_fields = ['title']
    inlines = [CommentInLineAdmin,PostInLineAdmin]
    empty_value_display = 'Unknown Item field'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','create_time','avatar','is_enable','parent']
   

admin.site.register(Product,PostFileAdmin)
admin.site.register(Category,CategoryAdmin)
