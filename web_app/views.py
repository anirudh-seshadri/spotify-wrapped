from os import access

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
from django.shortcuts import redirect
from django.conf import settings
import base64
import json
from requests import post, get

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

# Takes user to Spotify's auth url
def spotify_authentication(request):
    scope = 'user-read-private user-read-email user-top-read user-read-recently-played user-library-read' # Access to reading profile data, email address, top tracks that they have played
    host = request.get_host().replace('127.0.0.1', 'localhost')
    redirect_uri = f'http://{host}/back/'  # Builds the redirect URI and takes to back endpoint
    auth_url = f'{SPOTIFY_AUTH_URL}?client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}&scope={scope}' # client ID, auth code, uri to get redirected after login, scope

    return redirect(auth_url)

def spotify_back(request):
    error = request.GET.get('error') # Error parameter sent by spotify
    if error:
        state = request.GET.get('state') # State parameter sent by spotify
        return HttpResponse("Error occured while logging into spotify: ", state)

    code = request.GET.get('code') # Code parameter sent by spotify
    redirect_uri = request.build_absolute_uri('/back/')
    print(f"Callback Redirect URI: {redirect_uri}")
    auth_token = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    auth_base64str = str(base64.b64encode(auth_token.encode('utf-8')), 'utf-8') # Client credentials as base-64 encoded string

    # headers and data for post request for spotify token url
    headers = {'Authorization': f'Basic {auth_base64str}', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}
    response = post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
    tokens = json.loads(response.text) # access and refresh tokens for accessing spotify api

    # Tokens stored
    request.session['access_token'] = tokens['access_token']
    request.session['refresh_token'] = tokens['refresh_token']

    print("Tokens: ", tokens)

    return redirect('/')

# # Using access token, get data through spotify's api
def get_user_profile(request):
    try:
        access_token = request.session.get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'} # bearer is authorized to make api requests
        response = get(f'{SPOTIFY_API_BASE_URL}/me', headers=headers) # gets user's profile information
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
def get_top_tracks(request):
    try:
        access_token = request.session.get('access_token')
        time_range = request.GET.get('time_range', 'medium_term')
        lim = request.GET.get('limit', '20')
        headers = {'Authorization': f'Bearer {access_token}'}
        response = get(
            f'{SPOTIFY_API_BASE_URL}/me/top/tracks',
            headers=headers,
            params={'time_range': time_range, 'limit': lim}
        )
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_top_artists(request):
    try:
        access_token = request.session.get('access_token')
        time_range = request.GET.get('time_range', 'medium_term')
        lim = request.GET.get('limit', '20')
        headers = {'Authorization': f'Bearer {access_token}'}
        response = get(
            f'{SPOTIFY_API_BASE_URL}/me/top/artists',
            headers=headers,
            params={'time_range': time_range, 'limit': lim}
        )
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_recently_played(request):
    try:
        access_token = request.session.get('access_token')
        lim = request.GET.get('limit', '20')
        headers = {'Authorization': f'Bearer {access_token}'}
        response = get(
            f'{SPOTIFY_API_BASE_URL}/me/player/recently-played',
            headers=headers,
            params={'limit': lim}
        )
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_saved_tracks(request):
    try:
        access_token = request.session.get('access_token')
        lim = request.GET.get('limit', '20')
        offset = request.GET.get('offset', '0')
        headers = {'Authorization': f'Bearer {access_token}'}
        response = get(
            f'{SPOTIFY_API_BASE_URL}/me/tracks',
            headers=headers,
            params={'limit': lim, 'offset': offset}
        )
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_track_features(request, track_id):
    try:
        access_token = request.session.get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'}
        response = get(
            f'{SPOTIFY_API_BASE_URL}/audio-features/{track_id}',
            headers=headers
        )
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
def index(request):
    context = {
        'greeting' : 'How are you, user?'
    }
    return render(request, 'index.html', context)

def validate_spotify_id(request, id, type):
    # Ensure type is valid
    if type not in ['artist', 'album', 'playlist', 'track']:
        return JsonResponse({'error': 'Invalid type specified'}, status=400)

    # Get access token from session
    access_token = request.session.get('access_token')

    if not access_token:
        return JsonResponse({'error': 'Access token not found'}, status=400)

    # Set up the endpoint based on the type
    endpoint = f"{SPOTIFY_API_BASE_URL}/{type}s/{id}"

    # Set up headers with Authorization
    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        # Make the GET request to Spotify API
        response = get(endpoint, headers=headers)

        # Check if the response is valid
        if response.status_code == 200:
            return JsonResponse({'valid': True})
        elif response.status_code == 404:
            return JsonResponse({'valid': False})
        else:
            return JsonResponse({'error': 'Spotify API request failed'}, status=response.status_code)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def welcome(request):
    return render(request, 'index.html')

def game(request):
    return render(request, 'game.html')

def game_intro(request):
    return render(request, 'gameintro.html')