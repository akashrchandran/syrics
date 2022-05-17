import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-d",
                    "--directory",
                    metavar="PATH",
                    help='directory for downloads'
                    )

parser.add_argument("URL",
                    metavar="URL",
                    nargs="?",
                    help=("URL to get lyrics from spotify"),
                    )

def parse_cmd(config: dict):
    args = parser.parse_args()
    if args.directory:
        config['download_path'] = args.directory
    return args.URL