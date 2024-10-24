from django.shortcuts import render
from django.http import HttpResponse
import os
from django.shortcuts import redirect
from django.conf import settings
import base64
import json
from requests import post, get

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize?'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

# Takes user to Spotify's auth url
def spotify_authentication(request):
    scope = 'user-read-private user-read-email user-top-read' # Access to reading profile data, email address, top tracks that they have played
    redirect_uri = request.build_absolute_uri('/back/') # Builds absolute URI and takes to back endpoint
    auth_url = f'{SPOTIFY_AUTH_URL}?client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}&scope={scope}' # client ID, auth code, uri to get redirected after login, scope

    return redirect(auth_url)
def spotify_back(request):
    code = request.GET.get('code') # Code parameter sent by spotify
    redirect_uri = request.build_absolute_uri('/back/')
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

    return redirect('/')
# Using access token, get data through spotify's api
def get_spotify_data(request):
    access_token = request.session.get['access_token']
    headers = {'Authorization': f'Bearer {access_token}'} # bearer is authorized to make api requests
    response = get(f'{SPOTIFY_API_BASE_URL}/me/top/tracks', headers=headers) # gets user's top tracks
    return json.loads(response.text)


SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

# Takes user to Spotify's auth url
def spotify_authentication(request):
    scope = 'user-read-private user-read-email user-top-read' # Access to reading profile data, email address, top tracks that they have played
    redirect_uri = request.build_absolute_uri('/back/') # Builds absolute URI and takes to back endpoint
    auth_url = f'{SPOTIFY_AUTH_URL}?client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}&scope={scope}' # client ID, auth code, uri to get redirected after login, scope

    return redirect(auth_url)

def spotify_back(request):
    error = request.GET.get('error') # Error parameter sent by spotify
    if error:
        state = request.GET.get('state') # State parameter sent by spotify
        print("Error occured while logging into spotify: ", state)
        return HttpResponse("Error occured while logging into spotify: ", state)

    code = request.GET.get('code') # Code parameter sent by spotify
    redirect_uri = request.build_absolute_uri('/back/')
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
# Using access token, get data through spotify's api
def get_spotify_data(request):
    access_token = request.session.get['access_token']
    headers = {'Authorization': f'Bearer {access_token}'} # bearer is authorized to make api requests
    response = get(f'{SPOTIFY_API_BASE_URL}/me/top/tracks', headers=headers) # gets user's top tracks
    return json.loads(response.text)
def index(request):
    context = {
        'greeting' : 'How are you, user?'
    }
    return render(request, 'index.html', context)

def welcome(request):
    return render(request, 'welcome.html')

def login(request):
    return render(request, 'login.html')

def login_form(request):
    # Placeholder for login form logic
    return render(request, 'login_form.html')

def signup_form(request):
    # Placeholder for signup form logic
    return render(request, 'signup_form.html')