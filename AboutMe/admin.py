# Django
from django.contrib import admin

# Local
from .models import About


class AboutAdmin(admin.ModelAdmin):
    list_display = ['id']
    readonly_fields = ('code',)


admin.site.register(About, AboutAdmin)
