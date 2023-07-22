from django.urls import path
from.views import register_v,create_user_v,login_v,logout_v
urlpatterns = [
    path('register/',register_v,name='register'),
    path('create/',create_user_v,name='create'),
    path('login/',login_v,name='login'),
    path('logout/',logout_v,name='logout'),
    
]