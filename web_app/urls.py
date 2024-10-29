from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login, name='login'),
    path('login/form/', views.login_form, name='login_form'),  # Ensure this line exists
    path('signup/form/', views.signup_form, name='signup_form'),  # Ensure this line exists
    path('pastwraps/', views.pastwraps, name='pastwraps'), 
]