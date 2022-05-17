import os
from tqdm import tqdm
from api import Spotify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from exceptions import ConfigNotFound
import re
from cli import parse_cmd

try:
    with open("config.json") as f:
        config = json.load(f)
except Exception as e:
    raise ConfigNotFound("Config file seems to be missing.") from e

cmd_url = parse_cmd(config)

logo = '''
     _______.____    ____ .______       __    ______     _______.
    /       |\   \  /   / |   _  \     |  |  /      |   /       |
   |   (----` \   \/   /  |  |_)  |    |  | |  ,----'  |   (----`
    \   \      \_    _/   |      /     |  | |  |        \   \    
.----)   |       |  |     |  |\  \----.|  | |  `----.----)   |   
|_______/        |__|     | _| `._____||__|  \______|_______/    
                                                                 

'''

auth_manager = SpotifyClientCredentials(
                client_id=config['client_id'],
                client_secret=config['client_secret']
            )
sp = spotipy.Spotify(auth_manager=auth_manager)

print("Logging in....")
os.system('cls' if os.name == 'nt' else 'clear')
client = Spotify(config['sp_dc'])


def get_album_tracks(album_id: str):
    album_data = sp.album(album_id)
    print(f"> Album: {album_data['name']}")
    print(f"> Artist: {album_data['artists'][0]['name']}")
    print(f"> Songs: {album_data['total_tracks']} Tracks")
    print("\n")
    return [tracks['id'] for tracks in album_data['tracks']['items']]


def get_playlist_tracks(playlist_id: str):
    play_data = sp.playlist(playlist_id)
    print(f"> Playlist: {play_data['name']}")
    print(f"> Owner: {play_data['owner']['display_name']}")
    print(f"> Songs: {play_data['tracks']['total']} Tracks")
    print("\n")
    return [tracks['track']['id'] for tracks in play_data['tracks']['items']]


def format_lrc(lyrics_json):
    lyrics = lyrics_json['lyrics']['lines']
    if lyrics_json['lyrics']['syncType'] == 'UNSYNCED' and not config['force_synced']:
        lrc = [lines['words'] for lines in lyrics]
    else:
        lrc = []
        for lines in lyrics:
            duration = int(lines['startTimeMs'])
            minutes, seconds = divmod(duration / 1000, 60)
            lrc.append(f'[{minutes:0>2.0f}:{seconds:.3f}] {lines["words"]}')
    return '\n'.join(lrc)


def sanitize_track_data(track_data: dict):
    album_data = track_data['album']
    artist_data = track_data['artists']
    del track_data['album']
    del track_data['artists']
    track_data['album_name'] = album_data['name']
    track_data['release_date'] = album_data['release_date']
    track_data['total_tracks'] = str(album_data['total_tracks']).zfill(2)
    track_data['track_number'] = str(track_data['track_number']).zfill(2)
    track_data['album_artist'] = ','.join(
        [artist['name'] for artist in album_data['artists']])
    track_data['artist'] = ','.join([artist['name'] for artist in artist_data])


def save_lyrics(lyrics, track_data):
    file_name = f"{rename_using_format(config['file_name'], track_data)}.lrc"
    with open(f"{config['download_path']}/{file_name}", "w+", encoding='utf-8') as f:
        f.write(lyrics)


def rename_using_format(string: str, data: dict):
    matches = re.findall('{(.+?)}', string)
    for match in matches:
        word = '{%s}' % match
        string = string.replace(word, str(data[match]))
    return string


def download_lyrics(track_ids: list):
    tracks_data = sp.tracks(track_ids)['tracks']
    if config['download_path'] and not os.path.exists(config['download_path']):
        os.mkdir(config['download_path'])
    unable = []
    for track in tqdm(tracks_data):
        sanitize_track_data(track)
        lyrics_json = client.get_lyrics(track['id'])
        if not lyrics_json:
            unable.append(track)
            continue
        save_lyrics(format_lrc(lyrics_json), track)

def main():
    print(logo)
    print('\n')
    account = client.get_me()
    print("Successfully Logged In as:")
    print("Name: " + account["display_name"])
    print("Country: " + account["country"])
    print('\n')
    link = cmd_url or input("Enter Link: ")
    if 'album' in link:
        track_ids = get_album_tracks(link)
    elif 'playlist' in link:
        track_ids = get_playlist_tracks(link)
    elif 'track' in link:
        track_ids = [link]
    else:
        print("Enter valid url!")
        exit(0)
    download_lyrics(track_ids)


if __name__ == "__main__":
    main()
