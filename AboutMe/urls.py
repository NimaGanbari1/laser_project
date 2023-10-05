# Django
from django.urls import path

# Local
from .views import About_v

# Third Party
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('', About_v, name="aboutus"),

]
