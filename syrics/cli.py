import argparse
import json
import os
import subprocess
import sys

parser = argparse.ArgumentParser()

parser.add_argument("-d",
                    "--directory",
                    metavar="PATH",
                    help='give path to download directory.'
                    )

parser.add_argument("-f",
                    "--force",
                    metavar="BOOLEAN",
                    default=True,
                    help='skip check for if it already downloaded and is available in directory. '
                    )

parser.add_argument("-c",
                    "--config",
                    nargs='?',
                    const="edit",
                    help='edit config file or reset it.'
                    )

parser.add_argument("-u",
                    "--user",
                    nargs='?',
                    const="current",
                    help="items to download from users account like playlist, tracks etc.",
                    choices=['current', 'album', 'play']
                    )

parser.add_argument("URL",
                    metavar="URL",
                    nargs="?",
                    help=("url of song, album or playlist from spotify."),
                    )


def parse_cmd():
    args = parser.parse_args()
    if args.user in ['current', 'current-playing']:
        args.URL = 'current'
    elif args.user in ['play', 'playlist']:
        args.URL = 'play'
    elif args.user in ['album']:
        args.URL = 'album'
    if args.config == 'edit':
        create_config()
    elif args.config in ["reset", "r"]:
        create_config(config_exists = False)
    elif args.config in ["open", "o"]:
        open_config()
    return args.URL, args.directory, args.force

def input_taker(config, key, question, string = True):
    print(question)
    print(f"[SAVED]: {str(config[key])[:50]}")
    if ans := input():
        config[key] = ans if string else bool(int(ans))

def check_config():
    global CONFIG_FILE
    OS_CONFIG = os.environ.get("APPDATA") if os.name == "nt" else os.path.join(os.environ["HOME"], ".config")
    CONFIG_PATH = os.path.join(OS_CONFIG, "syrics")
    CONFIG_FILE = os.path.join(CONFIG_PATH, "config.json")
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(CONFIG_PATH, exist_ok=True)
        create_config(config_exists=False)
    return CONFIG_FILE


def create_config(config_exists = True):
    print("Editing Config File...")
    print("To keep the current value just press enter!")
    config = {
        'sp_dc': "", 
        'download_path': "downloads", 
        'create_folder': True, 
        'album_folder_name': "{name} - {artists}", 
        'play_folder_name': "{name} - {owner}", 
        'file_name': "{track_number}. {name}",
        'synced_lyrics': True, 
        'force_download': False
    }
    if config_exists:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    input_taker(config, 'sp_dc', "Enter the sp_dc: ")
    input_taker(config, 'download_path', "Enter the download path: ")
    input_taker(config, 'create_folder', "create folder for album/playlists: (0: False, 1: True)", string=False)
    input_taker(config, 'album_folder_name', "Enter the album folder naming format: ")
    input_taker(config, 'play_folder_name', "Enter the playlist folder naming format: ")
    input_taker(config, 'file_name', "Enter the file naming format: ")
    input_taker(config, 'synced_lyrics', "Get synced lyrics: (0: False, 1: True)", string=False)
    input_taker(config, 'force_download', "Skip check for if it already exists: (0: False, 1: True)", string=False)
    with open(CONFIG_FILE, "w+") as f:
        f.write(json.dumps(config, indent=4))
    print("config sucessfully setup, run the program again.")
    sys.exit(1)

def open_config():
    if os.name == "nt":
        subprocess.call(["notepad", CONFIG_FILE])
    else:
        subprocess.call(["nano", CONFIG_FILE])
    sys.exit(1)