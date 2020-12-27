from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #    API to post the comment
    path('postComment', views.postComment, name ='postComment'),
    path('', views.bloggingHome, name='bloggingHome'),
    path('<str:slug>', views.bloggingPost, name='bloggingPost'),


   
]