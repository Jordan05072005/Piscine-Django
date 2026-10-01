import json
import tempfile

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("fixture")

    def handle(self, *args, **options):
        with open(options["fixture"], "r") as f:
            data = json.load(f)

        # correspondance pk -> nom de planète
        planet_names = {
            obj["pk"]: obj["fields"]["name"]
            for obj in data
            if obj["model"] == "ex09.planets"
        }

        # remplace chaque homeworld (numéro) par le nom de la planète
        for obj in data:
            if obj["model"] == "ex09.people":
                hw = obj["fields"].get("homeworld")
                if hw is not None:
                    obj["fields"]["homeworld"] = planet_names[hw]

        # écrit une copie temporaire convertie et la charge
        with tempfile.NamedTemporaryFile("w", suffix=".json") as tmp:
            json.dump(data, tmp)
            tmp.flush()
            call_command("loaddata", tmp.name)