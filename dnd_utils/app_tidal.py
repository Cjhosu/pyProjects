from flask import Flask, redirect, render_template, request, url_for
from pathlib import Path
import random
import tidalapi
import vlc


app = Flask(__name__)
app.secret_key = 'nkjfhq83jkhqfjkh34kjh'

SESSION_FILE = Path(__file__).parent / 'tidal_session.json'

tidal_session = tidalapi.Session()
if SESSION_FILE.exists():
    tidal_session.load_session_from_file(SESSION_FILE)

login_state = {'link': None, 'error': None}

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()

# Tidal playlist UUIDs - find these in each playlist's share URL:
# https://tidal.com/playlist/<uuid>
playlist_uris = {
        'battle': 'a40ba1da-bac7-4da8-b846-36aff23be105',
        'caves': '2e6f9507-e456-43e3-810a-24859a7848e3',
        'city': 'a2f6a234-daf4-4950-bed0-9fa3ebe4257b',
        'intro': '1ca9f25d-3e42-40e5-a95a-635504ec58b0',
        'tavern': '5daec519-8313-4578-9685-cc387167404d',
        'travel': 'f4c39461-0326-478f-9017-48e6cca3aa0d',
        'horror': '8836b08a-101f-46be-a3be-5cde56086c52',
        }


@app.route('/')
def login():
    if tidal_session.check_login():
        return redirect(url_for('switch_track'))
    start_login()
    return render_template('login_tidal.html', url=login_state['link'].verification_uri_complete)


def start_login():
    link_login, future = tidal_session.login_oauth()
    login_state['link'] = link_login
    login_state['error'] = None

    def on_done(fut):
        try:
            fut.result()
            tidal_session.save_session_to_file(SESSION_FILE)
        except Exception as e:
            login_state['error'] = str(e)

    future.add_done_callback(on_done)


@app.route('/login/check')
def login_check():
    if tidal_session.check_login():
        return redirect(url_for('switch_track'))
    if login_state['error']:
        return ('Login failed: {}'.format(login_state['error']), 400)
    if not login_state['link']:
        return redirect(url_for('login'))
    return render_template('login_tidal.html', url=login_state['link'].verification_uri_complete)


@app.route('/switchTrack', methods=['GET', 'POST'])
def switch_track():
    if not tidal_session.check_login():
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('index_tidal.html')

    name = request.form.get('playlist_pick')
    if not name:
        return ('No name param supplied')
    if name not in playlist_uris:
        return ('No matching playlist')

    playlist = tidal_session.playlist(playlist_uris[name])
    tracks = playlist.tracks()
    if not tracks:
        return ('Playlist is empty')

    track = random.choice(tracks)
    stream_url = track.get_url()

    player.stop()
    media = vlc_instance.media_new(stream_url)
    player.set_media(media)
    player.play()

    return redirect(url_for('switch_track', _external=True))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
