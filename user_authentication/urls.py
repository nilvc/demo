from django.contrib import admin
from django.urls import path
from .views import register,login,hello

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('hello/', hello),
]
