from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('spotify/login/', views.spotify_authentication, name='spotify_login'),
    path('back/', views.spotify_back, name='spotify_back'),
    path('', views.index, name='index'),
    
]