from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    #path('list/',ProductionList),
    #path('index/<int:page>/',index),
    path('indexdetail/<int:id>/',ProductDetail),
    path('comment/',SetComment),
    path('listsearch/',ProductSearch),
    path('',HomePage),
]
