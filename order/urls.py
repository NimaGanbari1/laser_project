# Django
from django.urls import path

# Local
from .views import Ok_Record

urlpatterns = [
    path('register/',Ok_Record,name='okrec'),

]