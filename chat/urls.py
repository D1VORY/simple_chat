from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/messages/', views.MessagesListView.as_view(), name='messages'),
    path('login/', views.loginPage, name = 'login'),
    path('register/', views.registerPage, name = 'register'),
    path('logout/', views.logoutUser, name = 'logout'),
]
