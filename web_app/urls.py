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
    path('api/validate-spotify-id/<str:type>/<str:id>/', views.validate_spotify_id, name='validate_spotify_id'),
    path('get-spotify-track/<str:track_id>/', views.get_spotify_track, name='get_spotify_track'),
    path('get_tracks/<str:content_type>/<str:query>/', views.get_tracks, name='get_tracks'),
    path('get_access_token/', views.get_access_token, name='get_access_token'),  # Endpoint for access token
    path('game/', views.game, name='game'),
    path('gameintro/', views.game_intro, name='gameintro'),
    path('pastwraps/', views.pastwraps, name='pastwraps'), 
    path('profile/', views.profile, name='profile'),
    path('top-artists/', views.top_artists, name="top_artists"),
    path('in-year-you/', views.in_year_you, name="in_year_you"),
    path('top-genres/', views.top_genres, name="top_genres"),
    path('guess-song/', views.guess_song, name="guess_song"),
    path('time/', views.time, name="time"),
    path('top-songs/', views.top_songs, name="top_songs"),
    path('aura/', views.aura, name="aura"),
    path('friends/', views.friends, name="friends"),
    path('api/music-personality/', views.get_music_personality, name='music_personality'),
    path('game-transition/', views.game_transition, name="game_transition"),
    path('llm-transition/', views.llm_transition, name="llm_transition"),
    path('generate-wrapped/', views.generate_wrapped, name='generate_wrapped'),
    path('get-wraps/', views.get_wraps, name='get-wraps'),
    path('delete-all-wraps/', views.delete_all_wraps, name='delete_all_wraps'),
]