from typing import List

import requests
from django.conf import settings

from riotgames.models import LoLRealm


class RiotGamesClient:
    def __init__(self):
        self.api_url = "https://br1.api.riotgames.com"
        self.headers = {
            "X-Riot-Token": settings.RIOT_KEY,
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get(self, endpoint: str, base_url: str = None, params: dict = None):
        return self.session.get(f"{base_url or self.api_url}/{endpoint}", params=params).json()

    def summoner_by_name(self, name: str) -> dict:
        return self.get(f"lol/summoner/v4/summoners/by-name/{name}")

    def summoner_by_puuid(self, puuid: str) -> dict:
        return self.get(f"lol/summoner/v4/summoners/by-puuid/{puuid}")

    def summoner_by_account(self, account_id: str) -> dict:
        return self.get(f"lol/summoner/v4/summoners/by-account/{account_id}")

    def summoner_by_id(self, summoner_id: str) -> dict:
        return self.get(f"lol/summoner/v4/summoners/{summoner_id}")

    def matches(self, puuid: str, start: int = 0, count: int = 20, start_time: int = None, end_time: int = None, queue: str = None, game_type: str = None) -> List[dict]:
        params = {
            "start": start,
            "count": count,
        }
        if start_time:
            params["startTime"] = start_time

        if end_time:
            params["endTime"] = end_time

        if queue:
            params["queue"] = queue

        if game_type:
            params["type"] = game_type

        return self.get(f"lol/match/v5/matches/by-puuid/{puuid}/ids", base_url="https://americas.api.riotgames.com", params=params)

    def match_detail(self, match_id: str) -> dict:
        return self.get(f"lol/match/v5/matches/{match_id}", base_url="https://americas.api.riotgames.com")


class LeagueOfLegendsClient(RiotGamesClient):
    @staticmethod
    def region_list() -> List[str]:
        return [
            "br",
            "eune",
            "euw",
            "jp",
            "kr",
            "lan",
            "las",
            "na",
            "oce",
            "tr",
            "ru",
        ]

    def seasons(self) -> dict:
        return self.session.get("https://static.developer.riotgames.com/docs/lol/seasons.json").json()

    def queues(self) -> dict:
        return self.session.get("https://static.developer.riotgames.com/docs/lol/queues.json").json()

    def maps(self) -> dict:
        return self.session.get("https://static.developer.riotgames.com/docs/lol/maps.json").json()

    def game_modes(self) -> dict:
        return self.session.get("https://static.developer.riotgames.com/docs/lol/gameModes.json").json()

    def game_types(self) -> dict:
        return self.session.get("https://static.developer.riotgames.com/docs/lol/gameTypes.json").json()

    def languages(self) -> dict:
        return self.session.get("https://ddragon.leagueoflegends.com/cdn/languages.json").json()

    def versions(self) -> dict:
        return self.session.get("https://ddragon.leagueoflegends.com/api/versions.json").json()

    def realm(self, region: str = "br") -> dict:
        return self.session.get(f"https://ddragon.leagueoflegends.com/realms/{region}.json").json()

    def champions(self, region: str = "br", language: str = "pt_BR", version: str = None) -> dict:
        if not version:
            realm = LoLRealm.objects.get(pk=region)
            version = realm.n_champion

        return self.session.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/champion.json").json()
