from os import access

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
import base64
import json
from requests import post, get

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

# Takes user to Spotify's auth url
def spotify_authentication(request):
    scope = 'user-read-private user-read-email user-top-read user-read-recently-played user-library-read streaming user-read-playback-state user-modify-playback-state' # Access to reading profile data, email address, top tracks that they have played
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
    
def get_tracks(request, content_type, query):
    access_token = request.session.get('access_token')

    limit = 50  
    headers = {'Authorization': f'Bearer {access_token}'}

    if content_type == 'artist':
        endpoint = f"https://api.spotify.com/v1/search?q=artist:{query}&type=track&limit={limit}"
    elif content_type == 'artistID':
        endpoint = f"https://api.spotify.com/v1/artists/{query}/albums?market=US&limit={limit}"
    elif content_type == 'playlist':
        endpoint = f"https://api.spotify.com/v1/search?q=playlist:{query}&type=track&limit={limit}"
    elif content_type == 'playlistID':
        endpoint = f"https://api.spotify.com/v1/playlists/{query}/tracks?limit={limit}"
    elif content_type == 'album':
        endpoint = f"https://api.spotify.com/v1/search?q=album:{query}&type=track&limit={limit}"
    elif content_type == 'albumID':
        endpoint = f"https://api.spotify.com/v1/albums/{query}/tracks?limit={limit}"
    elif content_type == 'top50':
        endpoint = f"https://api.spotify.com/v1/me/top/tracks?limit={limit}"
    elif content_type == 'liked':
        endpoint = f"https://api.spotify.com/v1/me/tracks?limit={limit}"
    else:
        return JsonResponse({"error": "Invalid content type specified"}, status=400)

    response = get(endpoint, headers=headers)

    if response.status_code == 200:
        data = response.json()

        track_data = []

        if content_type in ['artist', 'playlist', 'album']:
            tracks = data.get('tracks', {}).get('items', [])
            for track in tracks:
                track_item = {
                    "title": track.get("name"),
                    "artist": track["artists"][0]["name"] if track.get("artists") else "Unknown",
                    "uri": track.get("uri"),
                    "duration": track.get("duration_ms")
                }
                if not any(existing["title"] == track_item["title"] for existing in track_data):
                    track_data.append(track_item)

        elif content_type == 'artistID':
            albums = data.get('items', [])

            for album in albums:
                if album.get('album_group') != 'appears_on':
                    album_id = album.get('id')
                    tracks_endpoint = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
                    tracks_response = get(tracks_endpoint, headers=headers)

                    if tracks_response.status_code == 200:
                        tracks = tracks_response.json().get('items', [])
                        for track in tracks:
                            if len(track_data) >= 50: 
                                break
                            track_item = {
                                'title': track.get('name'),
                                'artist': track['artists'][0].get('name', 'Unknown') if track.get('artists') else 'Unknown',
                                'uri': track.get('uri'),
                                'duration': track.get('duration_ms')
                            }

                            # Avoid adding duplicates
                            if not any(existing['title'] == track_item['title'] for existing in track_data):
                                track_data.append(track_item)

                        if len(track_data) >= 50:  
                            break
        elif content_type in ['top50', 'albumID']:
            tracks = data.get('items', [])
            for track in tracks:
                track_item = {
                    "title": track.get("name"),
                    "artist": track["artists"][0]["name"] if track.get("artists") else "Unknown",
                    "uri": track.get("uri"),
                    "duration": track.get("duration_ms")
                }
                if not any(existing["title"] == track_item["title"] for existing in track_data):
                    track_data.append(track_item)

        elif content_type in ['liked', 'playlistID']:
            tracks = data.get('items', [])
            for track in tracks:
                track_item = {
                    "title": track['track'].get("name"),
                    "artist": track['track']["artists"][0]["name"] if track['track'].get("artists") else "Unknown",
                    "uri": track['track'].get("uri"),
                    "duration": track['track'].get("duration_ms")
                }

                if not any(existing["title"] == track_item["title"] for existing in track_data):
                    track_data.append(track_item)

        return JsonResponse({"tracks": track_data}, safe=False)
    else:
        # Handle error
        return JsonResponse({"error": "Failed to retrieve data from Spotify"}, status=response.status_code)


def get_spotify_track(request, track_id):
    endpoint = f"https://api.spotify.com/v1/tracks/{track_id}"
    access_token = request.session.get('access_token')

    headers = {'Authorization': f'Bearer {access_token}'}
    response = get(endpoint, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        song_data = {
            "song": f"{response_data['name']} - {response_data['artists'][0]['name']}",
            "uri": f"spotify:track:{track_id}",
            "duration": response_data['duration_ms']
        }
        return JsonResponse(song_data)
    else:
        return JsonResponse({"error": "Failed to fetch song data"}, status=500)

def get_access_token(request):
    access_token = request.session.get('access_token')  
    
    if access_token:
        return JsonResponse({'access_token': access_token})
    else:
        return JsonResponse({'error': 'Access token not found'}, status=400)

def welcome(request):
    return render(request, 'index.html')

def game(request):
    access_token = request.session.get('access_token')
    print('Access Token: ', access_token)

    if not access_token:
        return redirect('welcome')
    return render(request, 'game.html')

def game_intro(request):
    return render(request, 'gameintro.html')