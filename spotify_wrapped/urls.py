"""
URL configuration for spotify_wrapped project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from web_app import views

urlpatterns = [
    path("", include("web_app.urls")),
    path('spotify/login/', views.spotify_authentication, name='spotify_login'),
    path('spotify/back/', views.spotify_back, name='spotify_callback'),
    path("admin/", admin.site.urls),
    path('spotify/login/', views.spotify_authentication, name='spotify_login'),
    path('back/', views.spotify_back, name='spotify_back'),
    path('api/profile/', views.get_user_profile, name='get_user_profile'),
    path('api/top-tracks/', views.get_top_tracks, name='get_top_tracks'),
    path('api/top-artists/', views.get_top_artists, name='get_top_artists'),
    path('api/recently-played/', views.get_recently_played, name='get_recently_played'),
    path('api/saved-tracks/', views.get_saved_tracks, name='get_saved_tracks'),
    path('api/track-features/<str:track_id>/', views.get_track_features, name='get_track_features'),
]
