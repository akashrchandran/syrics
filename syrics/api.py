import requests
import spotipy

from syrics.totp import TOTP

from .exceptions import NoSongPlaying, NotValidSp_Dc, TOTPGenerationException

TOKEN_URL = 'https://open.spotify.com/api/token'
SERVER_TIME_URL = 'https://open.spotify.com/server-time'
SPOTIFY_HOME_PAGE_URL = "https://open.spotify.com/"
CLIENT_VERSION = "1.2.46.25.g7f189073"

HEADERS = {
                "accept": "application/json",
                "accept-language": "en-US",
                "content-type": "application/json",
                "origin": SPOTIFY_HOME_PAGE_URL,
                "priority": "u=1, i",
                "referer": SPOTIFY_HOME_PAGE_URL,
                "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                "spotify-app-version": CLIENT_VERSION,
                "app-platform": "WebPlayer",
            }


class Spotify:
    def __init__(self, dc_token: str) -> None:
        self.session = requests.Session()
        self.session.cookies.set('sp_dc', dc_token)
        self.session.headers.update(HEADERS)
        self.totp = TOTP()
        self.login()
        self.sp = spotipy.Spotify(self.token)

    def login(self):
        try:
            server_time_response = self.session.get("https://open.spotify.com/api/server-time")
            server_time = 1e3 * server_time_response.json()["serverTime"]
            totp = self.totp.generate(timestamp=server_time)
            params={
                "reason": "init",
                "productType": "web-player",
                "totp": totp,
                "totpVer": str(self.totp.version),
                "ts": str(server_time),
            }
        except Exception as e:
            raise TOTPGenerationException("Error generating TOTP, retry!") from e
        try:
            req = self.session.get(TOKEN_URL, params=params)
            token = req.json()
            self.token = token['accessToken']
            self.session.headers['authorization'] = f"Bearer {self.token}"
        except Exception as e:
            raise NotValidSp_Dc("sp_dc provided is invalid, please check it again!") from e

    def get_me(self):
        try:
            return self.sp.current_user()
        except Exception as e:
            raise NotValidSp_Dc("sp_dc provided is invalid, please check it again!") from e

    def get_current_song(self):
        try:
            return self.sp.currently_playing()
        except Exception as e:
            raise NoSongPlaying("No song is currently playing.") from e

    def get_lyrics(self, track_id: str):
        params = 'format=json&market=from_token'
        req = self.session.get(f'https://spclient.wg.spotify.com/color-lyrics/v2/track/{track_id}', params=params)
        return req.json() if req.status_code == 200 else None
    
    def album(self, album_id):
        return self.sp.album(album_id)
    
    def album_tracks(self, album_id, total):
        tracks = []
        for x in range(0, total, 50):
            album = self.sp.album_tracks(album_id, offset=x)
            tracks += [track['id'] for track in album['items']]
        tracks =  [x for x in tracks if x is not None]
        return tracks

    def playlist(self, playlist_id):
        return self.sp.playlist(playlist_id)
    
    def playlist_tracks(self, playlist_id, total):
        tracks = []
        for x in range(0, total, 100):
            play = self.sp.playlist_tracks(playlist_id, offset=x)
            tracks += [track['track']['id'] for track in play['items']]
        tracks =  [x for x in tracks if x is not None]
        return tracks
    
    def tracks(self, tracks):
        return self.sp.tracks(tracks)

    def search(self, q, type, limit):
        return self.sp.search(q=q, type=type, limit=limit)

    def select_user_playlist(self):
        playlist = self.sp.current_user_playlists()['items']
        for x, play in enumerate(playlist, start=1):
            print(f"{x}: {play['name']}")
        index = int(input("Enter the index of the playlist: "))
        return playlist[index-1]

    def select_user_album(self):
        albums = self.sp.current_user_saved_albums()['items']
        for x, album in enumerate(albums, start=1):
            print(f"{x}: {album['album']['name']}")
        index = int(input("Enter the index of the album: "))
        return albums[index-1]['album']
