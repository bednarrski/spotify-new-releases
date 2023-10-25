# IMPORTS

from api import spotify_api
import json
from datetime import datetime, timedelta
import re
from time import gmtime, strftime
import git
import requests
# https://gitpython.readthedocs.io/en/stable/intro.html

settings_file = './api/settings.txt'
albums_cache_file = './albums_cache.txt'

max_album_age = 4 #years


# REFRESHING THE TOKEN

access_token = spotify_api.refresh_token(settings_file)


# CHECK LAST SUCCESS

last_success_file = "/Users/bednar/Logs/spotify_news_last_success.txt"
datetime_format = "%Y-%m-%d %H:%M:%S"

f = open(last_success_file, "r")
last_success_datetime = datetime.strptime(f.read(), '%Y-%m-%d %H:%M:%S')
print(f"Last success: {last_success_datetime}")


# FUNCTION TO GET RECENT TRACKS USING API

SPOTIFY_API_URL = 'https://api.spotify.com/v1'
#AUTH_URL = 'https://accounts.spotify.com/api/token'

def get_recent_tracks(token, artist_id, release_date):
    """
    Get recent tracks for a given artist ID and release date.
    """
    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(f'{SPOTIFY_API_URL}/artists/{artist_id}/albums', headers=headers)
    tracks = []

    for album in response.json()['items']:
        album_release_date = (album['release_date'] + "-01-01")[:10]
        album_release_date = datetime.strptime(album_release_date, '%Y-%m-%d')
        if album_release_date > release_date:
            album_tracks_response = requests.get(f'{SPOTIFY_API_URL}/albums/{album["id"]}/tracks?limit=50', headers=headers)
            tracks.extend(album_tracks_response.json()['items'])

    return tracks


# FUNCTION TO GET LIKED ARTISTS

def get_liked_artists(token, verbose = False):
    spotify_request_url = 'https://api.spotify.com/v1/'

    next_request = spotify_request_url + 'me/following?type=artist&limit=10'
    artists_dict = {}

    while(True):
        next_request = next_request + '&access_token=' + token.strip()
        artists_json = spotify_api.spotify_request(next_request)

        if verbose:
            print('\n')
        artist_items = artists_json['artists']['items']
        for item in artist_items:
            if verbose:
                print(item['name']+' -> '+item['id'])
            artists_dict[item['name']] = item['id']

        next_request = artists_json['artists']['next']

        if verbose:
            print('\n')
        if not next_request:
            if verbose:
                print("---END---")
            break
            
    return artists_dict



# GETTING LIKED ARTISTS

liked_artists = get_liked_artists(access_token, False)

# Get recent tracks for each liked artist
all_recent_tracks = []
for artist in liked_artists.keys():
    artist_recent_tracks = get_recent_tracks(access_token, liked_artists[artist], last_success_datetime)
    all_recent_tracks.extend(artist_recent_tracks)

# Extract track URIs
track_uris = [track['uri'] for track in all_recent_tracks]

len(track_uris)


# GET PLAYLISTS

headers = {
    'Authorization': f'Bearer {access_token.strip()}',
}

response = requests.get(f'{SPOTIFY_API_URL}/me/playlists', headers=headers)
playlists = response.json()['items']

for pl in playlists:
    print(f"{pl['id']} : {pl['name']}")
    

# ITERATE THROUGH NEW ALBUMS AND ADD THEM TO MY PLAYLIST
    
max_tracks_per_request = 10
my_playlist = '5QtunQsOyazjCStL8KNz3U'
url = 'https://api.spotify.com/v1/users/piotr.bednarski/playlists/' + my_playlist + '/tracks?uris='
headers = {
    'Authorization' : 'Bearer ' + access_token.strip(),
    'Content-Type' : 'application/json'
}
url_full = url
for i in range(len(track_uris)):
    #print(track_uris[i])
    url_full = url_full + track_uris[i] + ','
    
    if (i%max_tracks_per_request == max_tracks_per_request-1) or (i == len(track_uris)-1):
        url_full = url_full[:-1]
        #print("Request!")
        r = requests.post(url_full, headers=headers)
        #print(r)
        print(r.status_code, r.reason)
        url_full = url
        
        
# STORE LAST SUCCESS DATE

last_success_datetime = datetime.now()

f = open(last_success_file, "w")
f.write(last_success_datetime.strftime(datetime_format))
f.close()

print(f"New success date: {last_success_datetime}")
