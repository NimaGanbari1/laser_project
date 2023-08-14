from django.urls import path
from.views import register_v,create_user_v,login_v,logout_v,Cart_v,Final_v,About_v
urlpatterns = [
    path('register/',register_v,name='user-register'),
    path('create/',create_user_v,name='user-create'),
    path('login/',login_v,name='    '),
    path('logout/',logout_v,name='user-logout'),
    path('cart/',Cart_v,name='user-cart'),
    path('final/',Final_v,name='cart-final'),
    path('about/',About_v,name="aboutus")
]