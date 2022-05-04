import json
import re
import requests
from exceptions import NotValidSp_Dc

LOGIN_URL = "https://open.spotify.com/"
API_URL = "https://api.spotify.com/v1"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
EASY_REGEX = r'<script id="config" data-testid="config" type="application/json">(\S+)</script>'


class Spotify:
	def __init__(self, dc_token: str) -> None:
		self.session = requests.Session()
		self.session.cookies.set('sp_dc', dc_token)
		self.session.headers['User-Agent'] = USER_AGENT
		self.login()

	def login(self):
		try:
			req = self.session.get('https://open.spotify.com/', allow_redirects=False)
			tokens = json.loads(re.search(EASY_REGEX, req.text)[1])
			self.session.headers['authorization'] = f"Bearer {tokens['accessToken']}"
		except Exception as e:
			raise NotValidSp_Dc("sp_dc provided is invalid, please check it again!") from e

	def get_me(self):
		req = self.session.get(f'{API_URL}/me')
		return req.json()

	def search(self, word):
		params = 'operationName=searchDesktop&variables={"searchTerm":"blindin","offset":0,"limit":10,"numberOfTopResults":5,"includeAudiobooks":false}&extensions={"persistedQuery":{"version":1,"sha256Hash":"19967195df75ab8b51161b5ac4586eab9cf73b51b35a03010073533c33fd11ae"}}'
		req = self.session.get('https://api-partner.spotify.com/pathfinder/v1/query', params=params)
		return req.json()
	
	def get_song(self, tackid):
		req = self.session.get('https://spclient.wg.spotify.com/metadata/4/track/83e83f75d8584027a3f0fcb9c0f1dff3?market=from_token')
		print(req.content)