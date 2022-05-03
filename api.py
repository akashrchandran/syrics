import json
import re
import requests

LOGIN_URL = "https://open.spotify.com/"
API_URL = "https://api.spotify.com/v1"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
EASY_REGEX = r'<script id="config" data-testid="config" type="application/json">(\S+)</script>'

with open("token.json") as f:
	token_file = json.load(f)

class Spotify:
	def __init__(self, dc_token: str) -> None:
		self.session = requests.Session()
		self.session.cookies.set('sp_dc', dc_token)
		self.session.headers['User-Agent'] = USER_AGENT
		self.session.headers['authorization'] = f"Bearer {token_file['accessToken']}"

	def login(self):
		req = self.session.get('https://open.spotify.com/')
		tokens = json.loads(re.search(EASY_REGEX, req.text)[1])
		with open("token.json", "w") as f:
			json.dump(tokens, f, indent=4)
		return

	def get_me(self):
		req = self.session.get(f'{API_URL}/me')
		return req.json()