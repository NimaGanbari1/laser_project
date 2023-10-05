# Django
from django.contrib import admin
# Local
from .models import Category, Product, Comment, Post_File


class CommentInLineAdmin(admin.TabularInline):
    model = Comment
    fields = ['id', 'text', 'user']
    extra = 0


class PostInLineAdmin(admin.TabularInline):
    model = Post_File
    fields = ['id', 'title', 'file_type', 'fil', 'is_enable']
    readonly_fields = ['create_time']
    extra = 0


@admin.register(Product)
class PostFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'uniqe_code', 'price',
                    'create_time', 'is_enable', 'list_of_amenities', 'is_active']

    def list_of_amenities(self, obj):
        return ([category.title for category in obj.categories.all()])
    list_of_amenities.short_description = 'Category'
    list_display_links = ['title', 'id']
    list_per_page = 5
    date_hierarchy = 'create_time'
    search_fields = ['title', 'uniqe_code', 'is_enable']
    list_filter = ['create_time']
    filter_horizontal = ['categories']
    search_fields = ['title']
    inlines = [CommentInLineAdmin, PostInLineAdmin]
    empty_value_display = 'Unknown Item field'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'avatar',
                    'is_enable', 'parent', 'create_time']
    empty_value_display = 'Unknown'
    list_per_page = 5
    date_hierarchy = 'create_time'
    search_fields = ['title']
