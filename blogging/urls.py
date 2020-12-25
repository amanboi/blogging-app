from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.bloggingHome, name='bloggingHome'),
   path('<str:slug>', views.bloggingPost, name='bloggingPost'),
   
]