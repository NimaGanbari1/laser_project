from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('products/', include('products.urls')),
    path('users/', include('users.urls')),
    path('order/', include('order.urls')),
    path('',include('products.urls')),
    path('captcha',include("captcha.urls")),
    path('accounts/',include("allauth.urls")),
    
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
