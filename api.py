import json
import re

import requests
import spotipy

from exceptions import NotValidSp_Dc

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
EASY_REGEX = r'<script id="session" data-testid="session" type="application/json">(\S+)</script>'


class Spotify:
    def __init__(self, dc_token: str) -> None:
        self.session = requests.Session()
        self.session.cookies.set('sp_dc', dc_token)
        self.session.headers['User-Agent'] = USER_AGENT
        self.session.headers['app-platform'] = 'WebPlayer'
        self.login()
        self.sp = spotipy.Spotify(self.token)

    def login(self):
        try:
            req = self.session.get('https://open.spotify.com/', allow_redirects=False)
            token = json.loads(re.search(EASY_REGEX, req.text)[1])
            self.token = token['accessToken']
            self.session.headers['authorization'] = f"Bearer {self.token}"
        except Exception as e:
            raise NotValidSp_Dc("sp_dc provided is invalid, please check it again!") from e

    def get_me(self):
        return self.sp.current_user()

    def get_current_song(self):
        return self.sp.currently_playing()

    def get_lyrics(self, track_id: str):
        params = 'format=json&market=from_token'
        req = self.session.get(f'https://spclient.wg.spotify.com/color-lyrics/v2/track/{track_id}', params=params)
        return req.json()
    
    def album(self, album_id):
        return self.sp.album(album_id)

    def playlist(self, playlist_id):
        return self.sp.playlist(playlist_id)
    
    def tracks(self, tracks):
        return self.sp.tracks(tracks)

    def search(self, q, type, limit):
        return self.sp.search(q=q, type=type, limit=limit)