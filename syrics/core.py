#!/usr/bin/env python3
import json
import os
import re

from tinytag import TinyTag
from tqdm import tqdm

from syrics.api import Spotify
from syrics.cli import parse_cmd, check_config
from syrics.exceptions import CorruptedConfig

logo = '''
     _______.____    ____ .______       __    ______     _______.
    /       |\   \  /   / |   _  \     |  |  /      |   /       |
   |   (----` \   \/   /  |  |_)  |    |  | |  ,----'  |   (----`
    \   \      \_    _/   |      /     |  | |  |        \   \    
.----)   |       |  |     |  |\  \----.|  | |  `----.----)   |   
|_______/        |__|     | _| `._____||__|  \______|_______/    
                                                                 

'''


def get_album_tracks(album_id: str):
    album_data = client.album(album_id)
    album_data['artists'] = ','.join([artist['name'] for artist in album_data['artists']])
    album_folder = rename_using_format(config['album_folder_name'], album_data)
    print(f"> Album: {album_data['name']}")
    print(f"> Artist: {album_data['artists']}")
    print(f"> Songs: {album_data['total_tracks']} Tracks", end='\n\n')
    return client.album_tracks(album_id, album_data['total_tracks']), album_folder


def get_playlist_tracks(playlist_id: str):
    play_data = client.playlist(playlist_id)
    play_data['owner'] = play_data['owner']['display_name']
    play_data['total_tracks'] = play_data['tracks']['total']
    play_data['collaborative'] = '[C]' if play_data['collaborative'] else ''
    play_folder = rename_using_format(config['play_folder_name'], play_data)
    print(f"> Playlist: {play_data['name']}")
    print(f"> Owner: {play_data['owner']}")
    print(f"> Songs: {play_data} Tracks", end='\n\n')
    return client.playlist_tracks(playlist_id, play_data['tracks']['total']), play_folder


def format_lrc(lyrics_json, track_data):
    lyrics = lyrics_json['lyrics']['lines']
    minutes, seconds = divmod(int(track_data["duration_ms"]) / 1000, 60)
    lrc = [
        f'[ti:{track_data["name"]}]',
        f'[al:{track_data["album_name"]}]',
        f'[ar:{track_data["artist"]}]',
        f'[length: {minutes:0>2.0f}:{seconds:05.2f}]',
    ]
    for lines in lyrics:
        if lyrics_json['lyrics']['syncType'] == 'UNSYNCED' or not config['synced_lyrics']:
            lrc.append(lines['words'])
        else:
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
    track_data['explicit'] = '[E]' if track_data['explicit'] else ''


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
        if config['create_folder'] and not os.path.exists(folder) and config.get('force_download'):
            os.makedirs(folder, exist_ok=True)
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
        save_lyrics(format_lrc(lyrics_json, track), path=file_name)
    return unable

def fetch_files(path: str):
    files = [tracks for tracks in os.listdir(path) if re.search("\.(flac|mp3|wav|ogg|opus|m4a|aiff)$", tracks)]
    unable = []
    for files in tqdm(files):
            tag = TinyTag.get(os.path.join(path, files))
            query = client.search(q=f"track:{tag.title} album:{tag.album}", type="track", limit=1)
            if track := query['tracks']['items']:
                sanitize_track_data(track[0])
                file_name = f"{os.path.splitext(tag._filehandler.name)[0]}.lrc"
                lyrics_json = client.get_lyrics(track[0]['id'])
                if not lyrics_json:
                    unable.append(tag.title)
                    continue
                if not os.path.exists(file_name) and config.get('force_download'):
                    save_lyrics(format_lrc(lyrics_json, track[0]), path=file_name)
            else:
                unable.append(tag.title)
    return unable

def initial_checks():
    global client, cmd_url, config
    CONFIG_FILE = check_config()
    cmd_url, directory, force = parse_cmd()
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    except Exception as e:
        raise CorruptedConfig("Config file seems corrupted, run syrics -c reset") from e
    config['download_path'] = directory or config['download_path']
    config['force_download'] = force or config['force_download']
    client = Spotify(config['sp_dc'])
    if cmd_url == 'current':
        cmd_url = client.get_current_song( )['item']['external_urls']['spotify']
    elif cmd_url == 'play':
        cmd_url = client.select_user_playlist()['external_urls']['spotify']
    elif cmd_url == 'album':
        cmd_url = client.select_user_album()['external_urls']['spotify']

def main():
    initial_checks()
    if config['download_path'] and not os.path.exists(config['download_path']):
        os.mkdir(config['download_path'])
    print(logo, end='\n\n')
    account = client.get_me()
    print("Successfully Logged In as:")
    print("Name: " + account["display_name"])
    print("Country: " + account["country"], end='\n\n')
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
