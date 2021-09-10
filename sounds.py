import random
import requests
import os
import json

CLIENT_ID = '66c04c7baca048e79140bff763e7afdb'
CLIENT_SECRET = os.environ.get('SPOTIFY_KEY')
# set this to system and pull from env var

AUTH_URL = 'https://accounts.spotify.com/api/token'
playlist_uris = { 'battle': '6VtMoUfVW9p6yxKmeKPfrc', 'city' : '61ouQPvyL26ty8Yhssz5y2', 'intro' : '6rrIaBgm0lEB6SBE0T5x6d', 'tavern' : '6ll0DqazPBbPEWKtiRCLw1', 'travel' : '5w9YOt0lVo09gMyhyh4Pv2' }
print('\nWelcome to the sound board!\n')

auth_response = requests.post(AUTH_URL, {
    'grant_type' : 'client_credentials',
    'client_id' : CLIENT_ID,
    'client_secret' : CLIENT_SECRET
    })

auth_response_data = auth_response.json()

user_auth = requests.get('https://accounts.spotify.com/authorize', {
    'response_type' : 'token',
    'redirect_uri' : 'https://example.com/callback',
    'client_id' : CLIENT_ID,
    'scope' : 'user-read-private user-read-playback-state user-modify-playback-state'
    })

print(user_auth.url + '\n')

token = input('Enter token from successful url \n')

headers = {
        'Authorization': 'Bearer {token}'.format(token=token),
}
while True:
    pick = input('\nWhich playlist?\n')
    if str(pick) in list(playlist_uris.keys()):
        r = requests.get('https://api.spotify.com/v1/playlists/' + playlist_uris[pick] + '/tracks', headers = headers, params={"fields" : "total"})
        playlist_data = json.loads(r.text)
        count = dict(playlist_data)['total']
        if count == 1:
            starting = 0
        else:
            starting = random.randint(0,count -1)

        payload = {
                'context_uri' : 'spotify:playlist:'+ playlist_uris[pick],
                'offset': {
                    'position' : starting
                    }
                }

        play = requests.put('https://api.spotify.com/v1/me/player/play', headers = headers, data= json.dumps(payload))

    elif pick == '':
        print('exit \n')
        break
    else:
        print('pick a valid option \n')
