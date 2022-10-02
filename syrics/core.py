#!/usr/bin/env python3
import json
import os
from platform import platform
import re

from tinytag import TinyTag
from tqdm import tqdm

from syrics.api import Spotify
from syrics.cli import parse_cmd, create_config
from syrics.exceptions import CorruptedConfig

platform = os.name == "nt"
if platform:
    OS_CONFIG = os.environ.get("APPDATA")
else:
    OS_CONFIG = os.path.join(os.environ["HOME"], ".config")

CONFIG_PATH = os.path.join(OS_CONFIG, "syrics")
CONFIG_FILE = os.path.join(CONFIG_PATH, "config.json")
if not os.path.isdir(CONFIG_PATH) or not os.path.isfile(CONFIG_FILE):
        os.makedirs(CONFIG_PATH, exist_ok=True)
        create_config(CONFIG_FILE)

try:
    with open(CONFIG_FILE) as f:
        config = json.load(f)
except Exception as e:
    raise CorruptedConfig("Config file seems corrupted") from e

logo = '''
     _______.____    ____ .______       __    ______     _______.
    /       |\   \  /   / |   _  \     |  |  /      |   /       |
   |   (----` \   \/   /  |  |_)  |    |  | |  ,----'  |   (----`
    \   \      \_    _/   |      /     |  | |  |        \   \    
.----)   |       |  |     |  |\  \----.|  | |  `----.----)   |   
|_______/        |__|     | _| `._____||__|  \______|_______/    
                                                                 

'''

client = Spotify(config['sp_dc'])
cmd_url = parse_cmd(config, client)
print("Logging in....")
os.system('cls' if platform else 'clear')

def get_album_tracks(album_id: str):
    album_data = client.album(album_id)
    album_data['artists'] = ','.join([artist['name'] for artist in album_data['artists']])
    album_folder = rename_using_format(config['album_folder_name'], album_data)
    print(f"> Album: {album_data['name']}")
    print(f"> Artist: {album_data['artists']}")
    print(f"> Songs: {album_data['total_tracks']} Tracks")
    print("\n")
    return client.album_tracks(album_id, album_data['total_tracks']), album_folder


def get_playlist_tracks(playlist_id: str):
    play_data = client.playlist(playlist_id)
    play_data['owner'] = play_data['owner']['display_name']
    play_folder = rename_using_format(config['play_folder_name'], play_data)
    print(f"> Playlist: {play_data['name']}")
    print(f"> Owner: {play_data['owner']}")
    print(f"> Songs: {play_data['tracks']['total']} Tracks")
    print("\n")
    return client.playlist_tracks(playlist_id, play_data['tracks']['total']), play_folder


def format_lrc(lyrics_json):
    lyrics = lyrics_json['lyrics']['lines']
    if (lyrics_json['lyrics']['syncType'] == 'UNSYNCED' and not config['force_synced']) or not config['synced_lyrics']:
        lrc = [lines['words'] for lines in lyrics]
    else:
        lrc = []
        for lines in lyrics:
            duration = int(lines['startTimeMs'])
            minutes, seconds = divmod(duration / 1000, 60)
            lrc.append(f'[{minutes:0>2.0f}:{seconds:05.2f}] {lines["words"]}')
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


def save_lyrics(lyrics, path):
    with open(path, "w+", encoding='utf-8') as f:
        f.write(lyrics)


def rename_using_format(string: str, data: dict):
    matches = re.findall('{(.+?)}', string)
    for match in matches:
        word = '{%s}' % match
        string = string.replace(word, str(data[match]))
    return re.sub(r'[\\/*?:"<>|]',"", string)

def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def download_lyrics(track_ids: list, folder: str = None):
    unable = []
    if folder:
        folder = f"{config['download_path']}/{folder}"
        if config['create_folder'] and not os.path.exists(folder):
            os.mkdir(folder)
        else:
            print("The album/playlist was already downloaded..skipping")
            exit(0)
    else:
        folder = config['download_path']
    tracks_data = []
    for trackid in chunk(track_ids, 50):
        tracks_data += client.tracks(trackid)['tracks']
    for track in tqdm(tracks_data):
        sanitize_track_data(track)
        lyrics_json = client.get_lyrics(track['id'])
        if not lyrics_json:
            unable.append(track['name'])
            continue
        file_name = f"{folder}/{rename_using_format(config['file_name'], track)}.lrc"
        save_lyrics(format_lrc(lyrics_json), path=file_name)
    return unable

def fetch_files(path: str):
    files = [tracks for tracks in os.listdir(path) if re.search("\.(flac|mp3|wav|ogg|opus|m4a|aiff)$", tracks)]
    unable = []
    for files in tqdm(files):
            tag = TinyTag.get(os.path.join(path, files))
            query = client.search(q=f"track:{tag.title} album:{tag.album}", type="track", limit=1)
            if track := query['tracks']['items']:
                file_name = f"{os.path.splitext(tag._filehandler.name)[0]}.lrc"
                lyrics_json = client.get_lyrics(track[0]['id'])
                if not lyrics_json:
                    unable.append(tag.title)
                    continue
                save_lyrics(format_lrc(lyrics_json), path=file_name)
            else:
                unable.append(tag.title)
    return unable
                
def main():
    if config['download_path'] and not os.path.exists(config['download_path']):
        os.mkdir(config['download_path'])
    print(logo)
    print('\n')
    account = client.get_me()
    print("Successfully Logged In as:")
    print("Name: " + account["display_name"])
    print("Country: " + account["country"])
    print('\n')
    link = cmd_url or input("Enter Link: ")
    if 'spotify' in link:
        if 'album' in link:
            track_ids, folder = get_album_tracks(link)
        elif 'playlist' in link:
            track_ids, folder= get_playlist_tracks(link)
        elif 'track' in link:
            track_ids = [link]
            folder = None
        else:
            print("Enter valid url!")
            exit(0)
        unable = download_lyrics(track_ids, folder)
    else:
        unable = fetch_files(link)
    if unable:
        print("\nsome tracks does not have lyrics, so skipped:")
        for tracks in unable:
            print(tracks)
