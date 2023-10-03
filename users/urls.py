from django.urls import path
from.views import Final_v,About_v,Profile_v,delete_v,ForgotPassword_v,SetPassword_v,SetCode_v
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('final/',Final_v,name='cart-final'),
    path('about/',About_v,name="aboutus"),
    path('profile/',Profile_v,name="aboutus"),
    path('delete/',delete_v,name="delete-user"),
    path('forget/',ForgotPassword_v,name="forget-password"),
    path('setpass/',SetPassword_v,name="set-password"),
    path('setcode/',SetCode_v,name="set-code"),
    path('bankgateways/', az_bank_gateways_urls()),
]