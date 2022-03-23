import requests


class PubgClient:
    def __init__(self):
        self.api_url = "https://api.pubg.com/shards/steam"
        self.api_version = "v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/vnd.api+json",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    @property
    def api_key(self):
        from pubg.models import Token

        token = Token.objects.filter().order_by("?").first().token
        return token

    def get_player(self, player_id: str):
        return self.session.get(f"{self.api_url}/players/{player_id}").json()

    def get_match(self, match_id: str):
        return self.session.get(f"{self.api_url}/matches/{match_id}").json()
