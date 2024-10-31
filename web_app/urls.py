from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login, name='login'),
    path('login/form/', views.login_form, name='login_form'), 
    path('signup/form/', views.signup_form, name='signup_form'),
]