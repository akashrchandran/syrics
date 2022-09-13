import argparse

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
