import json
import re
import requests
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

    def login(self):
        try:
            req = self.session.get('https://open.spotify.com/', allow_redirects=False)
            tokens = json.loads(re.search(EASY_REGEX, req.text)[1])
            self.session.headers['authorization'] = f"Bearer {tokens['accessToken']}"
        except Exception as e:
            raise NotValidSp_Dc("sp_dc provided is invalid, please check it again!") from e

    def get_me(self):
        req = self.session.get('https://api.spotify.com/v1/me')
        return req.json()

    def get_lyrics(self, track_id: str):
        params = 'format=json&market=from_token'
        req = self.session.get(f'https://spclient.wg.spotify.com/color-lyrics/v2/track/{track_id}', params=params)
        return req.json()
    
    def get_current_song(self):
        req = self.session.get('https://api.spotify.com/v1/me/player/currently-playing')
        return req.json()
        