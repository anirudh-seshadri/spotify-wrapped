from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.conf import settings
import base64
import json
from requests import post, get
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'


# Register View
def register(request):
    if request.user.is_authenticated:
        # If user is already logged in, redirect to homepage
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Automatically log the user in after registration
        login(request, user)

        # Redirect to Home
        return redirect('/')

    return render(request, 'test_register.html')


# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'test_login.html')


# Logout View
def logout_view(request):
    logout(request)
    request.session.flush()
    cookies = request.COOKIES  # Access the cookies
    cookie_list = []
    for key, value in cookies.items():
        cookie_list.append(f"{key}: {value}")
    
    print("Cookies:")
    print(cookies)
    print(cookie_list)
    return redirect('login')


# Takes user to Spotify's auth url
def spotify_authentication(request):
    if not request.user.is_authenticated:
        return redirect('login')

    scope = 'user-read-private user-read-email user-top-read'
    redirect_uri = request.build_absolute_uri('/back/')
    auth_url = f'{SPOTIFY_AUTH_URL}?client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}&scope={scope}'

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
    print(f"Callback Redirect URI: {redirect_uri}")
    auth_token = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    auth_base64str = str(base64.b64encode(auth_token.encode('utf-8')), 'utf-8')

    headers = {'Authorization': f'Basic {auth_base64str}', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}
    response = post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
    tokens = json.loads(response.text)

    # Store tokens in the user's session
    #request.session['access_token'] = tokens['access_token']
    #request.session['refresh_token'] = tokens['refresh_token']
    #request.session['time_obtained'] = timezone.now().timestamp()  # Store time the token was obtained
    #request.session['expires_in'] = tokens['expires_in']

    # Store tokens in the User model
    user = request.user
    user.access_token = tokens['access_token']
    user.refresh_token = tokens['refresh_token']
    user.time_obtained = timezone.now()  # Store the time the token was obtained in the database
    user.expires_in = tokens['expires_in']
    user.save()

    # Redirect to the original page the user was trying to access
    next_url = request.session.pop('next', '/')  # Default to home page if 'next' is not set
    return redirect(next_url)

# Fetch Spotify user data
def get_spotify_data(request):
    access_token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = get(f'{SPOTIFY_API_BASE_URL}/me/top/tracks', headers=headers)
    return json.loads(response.text)

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

def welcome(request):
    return render(request, 'index.html')
