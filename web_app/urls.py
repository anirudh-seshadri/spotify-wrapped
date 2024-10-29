from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('slide1/', views.slide1, name='slide1'),
    path('slide2/', views.slide2, name='slide2'),
    path('slide3/', views.slide3, name='slide3'),
]