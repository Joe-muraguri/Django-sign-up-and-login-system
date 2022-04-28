from django import views
from django.urls import path
from .import views

urlpatterns = [


    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('products/', views.products, name='products'),
    path('member/<str:pk_test>/', views.member, name="member"),
]
