from django.contrib import admin
from .models import Category , Product, Comment , Post_File

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
    list_display = ['id','title','uniqe_code','price','create_time','is_enable','is_active']
    list_filter = ['create_time']
    filter_horizontal = ['categories']
    search_fields = ['title']
    inlines = [CommentInLineAdmin,PostInLineAdmin]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','create_time','avatar','is_enable','parent']
   

admin.site.register(Product,PostFileAdmin)
admin.site.register(Category,CategoryAdmin)
