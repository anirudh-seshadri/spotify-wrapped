from os import access
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
import base64
import json
from requests import post, get
from django.utils import timezone
import urllib.parse
from django.urls import reverse

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

# Register View
def register(request):
    if request.user.is_authenticated:
        # If user is already logged in, redirect to homepage
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('/register')

        # Create and save the new user
        user = User.objects.create_user(username=username, password=password)
        login(request, user)  # Log the user in after registration
        messages.success(request, 'Registration successful!')
        return redirect('/')  # Redirect to a 'home' page or any page you prefer

    return render(request, 'test_register.html')


# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        # Get username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            # Redirect to the home page or any other page
            return redirect('/')  # Replace 'home' with your desired URL name
        else:
            # Invalid credentials, add an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('/login')  # Redirect back to the login page

    return render(request, 'login.html')


# Logout View
def logout_view(request):
    if not request.user.is_authenticated:
        # If user is not logged in, redirect to login (can't logout if not logged in)
        return redirect('/login')

    logout(request)
    messages.info(request, "You have been logged out successfully.")
    
    print("Logging out user ", request.user)

    return redirect('/login')


# Takes user to Spotify's auth url
def spotify_authentication(request):
    if not request.user.is_authenticated:
        return redirect('login')

    scope = 'user-read-private user-read-email user-top-read'
    redirect_uri = request.build_absolute_uri(reverse('spotify_back'))
    params = {
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
    }
    auth_url = f'{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}'

    return redirect(auth_url)


# Handle Spotify authentication callback
def spotify_back(request):
    if not request.user.is_authenticated:
        return redirect('login')

    error = request.GET.get('error')
    if error:
        return HttpResponse(f"Error occurred during Spotify authentication: {error}")

    code = request.GET.get('code')
    redirect_uri = request.build_absolute_uri('/back/')
    auth_token = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    auth_base64str = str(base64.b64encode(auth_token.encode('utf-8')), 'utf-8')

    headers = {'Authorization': f'Basic {auth_base64str}', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}
    response = post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
    tokens = json.loads(response.text)

    # Store tokens in the user's session
    request.session['access_token'] = tokens['access_token']
    request.session['refresh_token'] = tokens['refresh_token']
    request.session['time_obtained'] = timezone.now().timestamp()  # Store time the token was obtained
    request.session['expires_in'] = tokens['expires_in']

    # Redirect to the original page the user was trying to access
    next_url = request.session.pop('next', '/')  # Default to home page if 'next' is not set
    return redirect(next_url)


def get_user_profile(request):
    print("Getting profile")
    try:
        access_token = request.session.get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'} # bearer is authorized to make api requests
        response = get(f'{SPOTIFY_API_BASE_URL}/me', headers=headers) # gets user's profile information

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

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

def welcome(request):
    return render(request, 'welcome.html')

def pastwraps(request):
    return render(request, 'pastwraps.html')

def profile(request):
    # Add login_required decorator if you want to restrict access to logged-in users only
    return render(request, 'profile.html')

def guess_song(request):
    return render(request, 'guess_song.html')
    
def top_artists(request):
    return render(request, 'top_artists.html')
    
def top_songs(request):
    return render(request, 'top_songs.html')

def time(request):
    return render(request, 'time.html')

def aura(request):
    return render(request, 'aura.html')

def friends(request):
    return render(request, 'friends.html')