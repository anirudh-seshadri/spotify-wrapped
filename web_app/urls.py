from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),  # Root URL shows welcome page
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('spotify/login/', views.spotify_authentication, name='spotify_login'),
    path('back/', views.spotify_back, name='spotify_back'),
    path('api/profile/', views.get_user_profile, name='get_user_profile'),
    path('api/top-tracks/', views.get_top_tracks, name='get_top_tracks'),
    path('api/top-artists/', views.get_top_artists, name='get_top_artists'),
    path('api/recently-played/', views.get_recently_played, name='get_recently_played'),
    path('api/saved-tracks/', views.get_saved_tracks, name='get_saved_tracks'),
    path('api/track-features/<str:track_id>/', views.get_track_features, name='get_track_features'),
    path('pastwraps/', views.pastwraps, name='pastwraps'), 
    path('profile/', views.profile, name='profile'),
    path('time/', views.time, name="time"),
    path('top-songs/', views.top_songs, name="top_songs"),
    path('aura/', views.aura, name="aura"),
    path('friends/', views.friends, name="friends")
]