import requests


class ThingiverseApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.thingiverse.com"

    def _get(self, url):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")
        return response.json()

    def get_thing(self, thing_id):
        return self._get(f"{self.base_url}/things/{thing_id}")

    def get_files(self, thing_id):
        return self._get(f"{self.base_url}/things/{thing_id}/files")
