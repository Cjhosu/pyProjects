from flask import Flask, redirect, render_template, request, session, url_for
import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time


app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'jfkqhiuqefakdnj'

TOKEN_INFO = 'token_info'
CLIENT_ID = '66c04c7baca048e79140bff763e7afdb'
CLIENT_SECRET = os.environ.get('SPOTIFY_KEY')

playlist_uris = {
        'battle': '6VtMoUfVW9p6yxKmeKPfrc',
        'caves': '7I4KwmekYEfA7MGw2HOszk',
        'city': '61ouQPvyL26ty8Yhssz5y2',
        'intro': '6rrIaBgm0lEB6SBE0T5x6d',
        'tavern': '6ll0DqazPBbPEWKtiRCLw1',
        'travel': '5w9YOt0lVo09gMyhyh4Pv2',
        'horror': '6tUoj6X0uf6HxJ6dqZKwnN'
        }


@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('switch_track', _external=True))


@app.route('/test')
def test():
    return ('TEST')


@app.route('/switchTrack', methods=['GET', 'POST'])
def switch_track():
    if request.method == 'GET':
        return render_template('index.html')
    try:
        token_info = get_token()
    except Exception:
        print("user not logged in")
        return redirect('/')
    if request.form.get('playlist_pick'):
        name = request.form.get('playlist_pick')
        if name in playlist_uris:
            playlist_id = playlist_uris[name]
            sp = spotipy.Spotify(auth=token_info['access_token'])
            current_playlists = sp.current_user_playlists()['items']
            for playlist in current_playlists:
                if playlist['id'] == playlist_id:
                    items = sp.playlist_items(playlist_id)
                    songs = items['items']
                    count = len(songs)
                    if count == 1:
                        starting = 0
                    else:
                        starting = random.randint(0, count - 1)
                    song_uri = songs[starting]['track']['uri']
                    sp.start_playback(uris=[song_uri])
                    return redirect(url_for('switch_track', _external=True))
        else:
            return ('OATH SUCCESSFUL - No matching playlist')
    else:
        return ('No name param supplied')


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', _external=False))

    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=url_for('redirect_page', _external=True),
            scope='user-read-private user-read-playback-state user-modify-playback-state'
            )


app.run(debug=True)
