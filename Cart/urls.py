from django.urls import path
from .views import Cart_v

urlpatterns = [
    path('', Cart_v, name='ca'),
]
