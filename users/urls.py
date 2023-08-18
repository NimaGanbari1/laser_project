from django.urls import path
from.views import register_v,create_user_v,login_v,logout_v,Cart_v,Final_v,About_v,Profile_v,delete_v,ForgotPassword_v,SetPassword_v,SetCode_v
urlpatterns = [
    path('register/',register_v,name='user-register'),
    path('create/',create_user_v,name='user-create'),
    path('login/',login_v,name='user-login'),
    path('logout/',logout_v,name='user-logout'),
    path('cart/',Cart_v,name='user-cart'),
    path('final/',Final_v,name='cart-final'),
    path('about/',About_v,name="aboutus"),
    path('profile/',Profile_v,name="aboutus"),
    path('delete/',delete_v,name="delete-user"),
    path('forget/',ForgotPassword_v,name="forget-password"),
    path('setpass/',SetPassword_v,name="set-password"),
    path('setcode/',SetCode_v,name="set-code"),
]