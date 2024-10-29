from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from requests import post
import json  # Importing the json module
from web_app.models import User

SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

class SpotifyAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Auth Middleware")
        
        
        # Skip authentication for certain paths like login, register, spotify login, and back
        normalized_path = request.path.rstrip('/')
        if normalized_path in ['/spotify/login', '/back', '/login', '/register']:
            return self.get_response(request)

        
        # Check if the user is logged in
        if not request.user.is_authenticated:
            print("User not logged in or registered")
            # Store the original path in session and redirect to login
            request.session['next'] = request.path
            return redirect('/login')

        # Check if the user has a valid Spotify access token
        user = request.user
        printUser(user)

        if user.access_token and user.time_obtained and user.expires_in:
            # Check if the token is still valid
            current_time = timezone.now()
            token_expiration_time = user.time_obtained + timedelta(seconds=user.expires_in)
            if current_time >= token_expiration_time:
                print("User has access token but needs refreshing")
                # Attempt to refresh the access token using the refresh token
                if user.refresh_token:
                    print("Attempting to refresh token")
                    new_tokens = refresh_spotify_token(user.refresh_token)
                    if new_tokens:
                        print("New tokens obtained after refreshing: ", new_tokens)
                        user.access_token = new_tokens['access_token']
                        user.expires_in = new_tokens['expires_in']
                        user.time_obtained = timezone.now()
                        user.save()
                    else:
                        return redirect('/spotify/login/')

        else:
            print("No access token, redirecting to Spotify login")
            print("Session Details: ", request.session.keys(), request.session.values())
            # No access token, redirect to Spotify login
            request.session['next'] = request.path
            return redirect('/spotify/login/')

        # Proceed to the next middleware/view
        print("Proceeding to next middleware/view: ", request.path)
        response = self.get_response(request)
        return response


def refresh_spotify_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    response = post(SPOTIFY_TOKEN_URL, data=data)
    if response.status_code == 200:
        return json.loads(response.text)  # Using json to parse the response text
    return None


def printUser(user: User):
    print("User: ")
    print("\tAccess Token: " + user.access_token[0:20] + "..." if user.access_token else "None")
    print("\tTime Obtained: " + str(user.time_obtained))
    print("\tExpires In: " + str(user.expires_in))
    print("\tRefresh Token: " + user.refresh_token[0:20] + "..." if user.refresh_token else "None")
    print("\tToken Expired: ", user.token_expired())
    print()
