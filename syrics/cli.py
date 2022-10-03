import argparse
import json
import os

parser = argparse.ArgumentParser()

parser.add_argument("-d",
                    "--directory",
                    metavar="PATH",
                    help='directory for downloads'
                    )

parser.add_argument("-c",
                    "--config",
                    nargs='?',
                    const="edit",
                    help='Edit/reset config file.'
                    )

parser.add_argument("-u",
                    "--user",
                    nargs='?',
                    const="current",
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
    if args.config == 'edit':
        create_config()
    elif args.config in ["reset", "r"]:
        create_config(False)
    return args.URL

def input_taker(config, key, question, string = True):
    print(question)
    print(f"[SAVED]: {str(config[key])[:20]}")
    if ans := input():
        config[key] = ans if string else bool(int(ans))

def create_config(config_exits = True):
    print("Editing Config File...")
    config = {
        'sp_dc': "", 
        'download_path': "downloads", 
        'create_folder': True, 
        'album_folder_name': "{name} - {artists}", 
        'play_folder_name': "{name} - {owner}", 
        'file_name': "{track_number}. {name}",
        'synced_lyrics': True, 
        'force_synced': False
    }
    if config_exits:
        OS_CONFIG = os.environ.get("APPDATA") if os.name == "nt" else os.path.join(os.environ["HOME"], ".config")
        CONFIG_PATH = os.path.join(OS_CONFIG, "syrics")
        CONFIG_FILE = os.path.join(CONFIG_PATH, "config.json")
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    input_taker(config, 'sp_dc', "Enter the sp_dc: ")
    input_taker(config, 'download_path', "Enter the download path: ")
    input_taker(config, 'create_folder', "create folder for album/playlists: (0: False, 1: True)", string=False)
    input_taker(config, 'album_folder_name', "Enter the album folder naming format: ")
    input_taker(config, 'play_folder_name', "Enter the playlist folder naming format: ")
    input_taker(config, 'file_name', "Enter the file naming format: ")
    input_taker(config, 'synced_lyrics', "Get synced lyrics: (0: False, 1: True)", string=False)
    input_taker(config, 'force_synced', "Only get synced lyrics: (0: False, 1: True)", string=False)
    with open(CONFIG_FILE, "w+") as f:
        f.write(json.dumps(config, indent=4))
    print("config sucessfully setup, run the program again.")
    exit(1)