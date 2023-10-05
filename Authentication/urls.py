# Django
from django.urls import path

# Third Party
from azbankgateways.urls import az_bank_gateways_urls

# Local
from .views import register_v, create_user_v, login_v, logout_v, ForgotPassword_v, SetCode_v, SetPassword_v

urlpatterns = [
    path('register/', register_v, name='user-register'),
    path('create/', create_user_v, name='user-create'),
    path('login/', login_v, name='user-login'),
    path('logout/', logout_v, name='user-logout'),
    path('forget/', ForgotPassword_v, name="forget-password"),
    path('setpass/', SetPassword_v, name="set-password"),
    path('setcode/', SetCode_v, name="set-code"),
]
