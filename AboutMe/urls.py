from django.urls import path
from .views import About_v
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('',About_v,name="aboutus"),
    
]
    