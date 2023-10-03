from azbankgateways.urls import az_bank_gateways_urls
from django.urls import path
from .views import register_v, create_user_v, login_v, logout_v

urlpatterns = [
    path('register/', register_v, name='user-register'),
    path('create/', create_user_v, name='user-create'),
    path('login/', login_v, name='user-login'),
    path('logout/', logout_v, name='user-logout'),
]
