import json
import os

from colorama import Fore, Style
from django.core.management.base import BaseCommand
from git import Repo

from game.models import Character


def cprint(color: Fore, text: str):
    print(color + text + Style.RESET_ALL)


class Command(BaseCommand):
    help = "Import game data"

    def handle(self, *args, **options):
        repo_path = "game/genshinapi"
        repo_url = "https://github.com/genshindev/api.git"

        repository = None
        if not os.path.exists(repo_path):
            cprint(Fore.GREEN, f"Clonning {repo_url} to {repo_path}")
            repository = Repo.clone_from(repo_url, "game/genshinapi", depth=1)

        if not repository:
            cprint(Fore.GREEN, "Updating the local repository...")
            repository = Repo(repo_path)
            repository.git.pull()

        characters_path = os.listdir("game/genshinapi/assets/data/characters")

        for character_path in characters_path:
            with open(
                f"game/genshinapi/assets/data/characters/{character_path}/en.json", "r"
            ) as f:
                data = json.load(f)

            cprint(Fore.GREEN, f'Updating {data["name"]}')
            character, _ = Character.objects.get_or_create(slug=character_path)
            character.name = data["name"]
            character.slug = character_path
            character.vision = data["vision"]
            character.weapon = data["weapon"]
            character.nation = data["nation"]
            character.affiliation = data["affiliation"]
            character.rarity = data["rarity"]
            character.constellation = data["constellation"]

            if data.get("birthday"):
                character.birthday = (
                    data.get("birthday", "").replace("0000-", "1972-") or None
                )
            character.description = data["description"]
            character.vision_key = data["vision_key"]
            character.weapon_type = data["weapon_type"]
            character.raw_data = data
            character.save()
