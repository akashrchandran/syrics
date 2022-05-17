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
