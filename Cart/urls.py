# Django
from django.urls import path

# Local
from .views import Cart_v, Final_v

# Third party
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('', Cart_v, name='ca'),
    path('final/', Final_v, name='cart-final'),
    path('bankgateways/', az_bank_gateways_urls()),

]
