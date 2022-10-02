import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument("-d",
                    "--directory",
                    metavar="PATH",
                    help='directory for downloads'
                    )

parser.add_argument("-u",
                    "--user",
                    help="items to download from users account (cuurent-playing, album, playlist)"
                    )

parser.add_argument("URL",
                    metavar="URL",
                    nargs="?",
                    help=("URL to get lyrics from spotify"),
                    )


def parse_cmd(config, client):
    args = parser.parse_args()
    if args.directory:
        config['download_path'] = args.directory
    if args.user in ['current', 'current-playing']:
        args.URL = client.get_current_song(
        )['item']['external_urls']['spotify']
    elif args.user in ['play', 'playlist']:
        args.URL = client.select_user_playlist()['external_urls']['spotify']
    elif args.user in ['album']:
        args.URL = client.select_user_album()['external_urls']['spotify']
    return args.URL

def create_config(CONFIG_FILE):
    print("Editing Config File...")
    config = {}
    config['sp_dc'] = input("Enter the sp_dc (https://github.com/akashrchandran/syrics/wiki/Finding-sp_dc): \n") or ""
    config['download_path'] = input("Enter the download path: \n") or "downloads"
    config['create_folder'] = bool(int(input("create folder for album/playlists: (0: False, 1: True)")))
    config['album_folder_name'] = input("Enter the album folder naming format: ") or "{name} - {artists}"
    config['album_folder_name'] = input("Enter the playlist folder naming format: ") or "{name} - {owner}"
    config['album_folder_name'] = input("Enter the file naming format: ") or "{track_number}. {name}"
    config['synced_lyrics'] = bool(int(input("Get synced lyrics: (0: False, 1: True)")))
    config['force_synced'] = bool(int(input("Only get synced lyrics: (0: False, 1: True)")))
    with open(CONFIG_FILE, "w+") as f:
        f.write(json.dumps(config, indent=4))