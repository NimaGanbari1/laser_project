from django.urls import path
from .views import Ok_Record

urlpatterns = [
    path('register/',Ok_Record,name='okrec'),

]