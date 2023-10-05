# Django
from django.urls import path
# local
from .views import Profile_v, delete_v

urlpatterns = [
    path('profile/', Profile_v, name="aboutus"),
    path('delete/', delete_v, name="delete-user"),
]
