# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def spotify_request(request):
    print("\nRequesting: {0}".format(request))
    
    url = request
    headers = {
    }
    r = requests.get(url, headers=headers)

    print(r.status_code, r.reason)
    resp = r.json()
    return resp

def refresh_token(settings_file):
    with open(settings_file, 'r') as f:
        lines = []
        for line in f.readlines():
            lines.append(line)
        access_token = lines[0]
        refresh_token = lines[1]
        client_id = lines[2]
        client_secret = lines[3]
        
    new_access_token = access_token
    
    request = ''
    print("\nRequesting refresh: {0}".format(request))   
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization' : 'Basic YjlkZGFjMzE0MzU1NGNmZTg2OWE1YTFmZDczNjM0ODU6YTJkYjQ0YTI3ZTkzNGI2ZWIxY2VhNDI1ZDE3M2RiMzI=',
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token.strip()
    }
    r = requests.post(url, headers=headers, data=payload)
    
    print(r)
    print(r.status_code, r.reason)
    resp = r.json()
    print(resp['access_token'])
    new_access_token = resp['access_token']
    
    print(new_access_token)
    
    with open(settings_file, 'w') as f:
        f.write(new_access_token+'\n')
        f.write(refresh_token)
        f.write(client_id)
        f.write(client_secret)
    
    return new_access_token

if __name__ == '__main__':
    
    access_token = refresh_token('./settings.txt')

    inputs = ['https://api.spotify.com/v1/me/' +'following?type=artist&access_token='+access_token.strip()]

    for sample_input in inputs:
        test = spotify_request(sample_input)
        #print(test)
