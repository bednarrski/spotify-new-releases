from api import spotify_api
import json
import datetime
import re
from time import gmtime, strftime
import git

settings_file = '/home/piotr.bednarski/Repositories/spotify-new-releases/api/settings.txt'
albums_cache_file = '/home/piotr.bednarski/Repositories/spotify-new-releases/albums_cache.txt'

max_album_age = 4 #years

# GETTING ACCESS TOKEN FROM REFRESH TOKEN

access_token = spotify_api.refresh_token(settings_file)

# GETTING FOLLOWED ARTISTS

spotify_request_url = 'https://api.spotify.com/v1/'

next_request = spotify_request_url + 'me/following?type=artist&limit=10'
artists_dict = {}

while(True):
    next_request = next_request + '&access_token=' + access_token.strip()
    artists_json = spotify_api.spotify_request(next_request)

    print('\n')
    artist_items = artists_json['artists']['items']
    for item in artist_items:
        print(item['name']+' -> '+item['id'])
        artists_dict[item['name']] = item['id']

    next_request = artists_json['artists']['next']
    
    print('\n')
    if not next_request:
        print("---END---")
        break
        
# GETTING ALBUMS OF THESE ARTISTS

albums_list = []
with open(albums_cache_file, 'r') as f:
    for album_id in f.readlines():
        albums_list.append(album_id.strip())

new_albums_dict = {}
new_album_counter = 0
current_year = datetime.datetime.now().year

with open(albums_cache_file, 'a') as f:
    for artist in artists_dict:
        artist_id = artists_dict[artist]
        print('\nArtist: ' + artist)

        next_request = spotify_request_url + 'artists/'+artist_id+'/albums?limit=50&album_type=album,single&market=PL'

        while(True):
            next_request = next_request + '&access_token=' + access_token.strip()
            albums_json = spotify_api.spotify_request(next_request)

            album_items = albums_json['items']
            for item in album_items:
                print(item['name']+' -> '+item['release_date'])
                if item['id'] not in albums_list:
                    if current_year - int(item['release_date'][:4]) < max_album_age:
                        new_albums_dict[item['id']] = (artist, item['name'], item['release_date'])
                        f.write(item['id']+'\n')
                        new_album_counter = new_album_counter + 1

            next_request = albums_json['next']
            if not next_request:
                break
                
print('New albums: ' + str(new_album_counter))

# GETTING THE SONGS

tracks_counter = 0
new_tracks = []

for album_id in new_albums_dict:
    next_request = spotify_request_url + 'albums/'+album_id+'/tracks?limit=50&access_token=' + access_token.strip()
    tracks_json = spotify_api.spotify_request(next_request)
    
    tracks_items = tracks_json['items']
    for item in tracks_items:
        print(item['name'] + ' -> ' + item['uri'])
        new_tracks.append(item['uri'].strip())
        tracks_counter = tracks_counter + 1
        
print('New tracks: ' + str(tracks_counter))

# GETTING THE RIGHT PLAYSLIST

next_request = 'https://api.spotify.com/v1/me/playlists?access_token=' + access_token.strip()
playlists_json = spotify_api.spotify_request(next_request)

my_playlist = '5QtunQsOyazjCStL8KNz3U'

playlists_items = playlists_json['items']
for item in playlists_items:
    print(item['name'] + ' -> ' + item['id'])
    if item['name'].strip() == 'Music News (Bednar)':
        my_playlist = item['id'].strip()
        
print('\nMy playlist ID: ' + my_playlist)

# UPLOADING THE PLAYLIST

import requests

max_tracks_per_request = 10
url = 'https://api.spotify.com/v1/users/piotr.bednarski/playlists/' + my_playlist + '/tracks?uris='
headers = {
    'Authorization' : 'Bearer ' + access_token.strip(),
    'Content-Type' : 'application/json'
}
url_full = url
for i in range(len(new_tracks)):
    #print(new_tracks[i])
    url_full = url_full + new_tracks[i] + ','
    
    if (i%max_tracks_per_request == max_tracks_per_request-1) or (i == len(new_tracks)-1):
        url_full = url_full[:-1]
        #print("Request!")
        r = requests.post(url_full, headers=headers)
        #print(r)
        print(r.status_code, r.reason)
        url_full = url
        
# CREATING FEED

with open('feed_stub.xml', 'r') as fs:
    feed_stub=fs.read()
    
title = strftime("%Y-%m-%d %H:%M Spotify newest releases", gmtime())
feed = re.sub('TITLE', title, feed_stub, flags=(re.MULTILINE | re.DOTALL))

description = 'New releases:&lt;br&gt;'
for item in new_albums_dict:
    description = description + '&lt;br&gt;' + new_albums_dict[item][0]+ ' - ' + new_albums_dict[item][1]
print(description)
feed = re.sub('DESCRIPTION', description, feed, flags=(re.MULTILINE | re.DOTALL))

with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write(feed)
    
# SENDING FEED TO THE GIT REPO

repo = git.Repo( '/home/piotr.bednarski/Repositories/spotify-new-releases' )
print(repo.git.add( '.' ))

timestring = strftime("%Y%m%d_%H%M%S", gmtime())
message = '"Update at ' + timestring + '"'

print(repo.git.commit( m=message ))
print(repo.git.push())
print(repo.git.status())