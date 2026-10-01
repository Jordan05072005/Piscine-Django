import json
import tempfile

from django.core.management import BaseCommand, call_command
from django.utils import timezone

APP = "ex10"
TIMESTAMPED = {f"{APP}.planets", f"{APP}.people"}


class Command(BaseCommand):
    help = "Charge la fixture ex10 : homeworld (pk -> name) et created/updated manquants"

    def add_arguments(self, parser):
        parser.add_argument("fixture")

    def handle(self, *args, **options):
        with open(options["fixture"], "r") as f:
            data = json.load(f)

        # correspondance pk -> nom de planète
        planet_names = {
            obj["pk"]: obj["fields"]["name"]
            for obj in data
            if obj["model"] == f"{APP}.planets"
        }

        now = timezone.now().isoformat()

        for obj in data:
            fields = obj["fields"]

            # remplace chaque homeworld (numéro) par le nom de la planète
            if obj["model"] == f"{APP}.people":
                hw = fields.get("homeworld")
                if isinstance(hw, int):
                    fields["homeworld"] = planet_names[hw]

            # ajoute created/updated s'ils sont absents (loaddata n'applique pas auto_now)
            if obj["model"] in TIMESTAMPED:
                fields.setdefault("created", now)
                fields.setdefault("updated", now)

        # écrit une copie temporaire convertie et la charge
        with tempfile.NamedTemporaryFile("w", suffix=".json") as tmp:
            json.dump(data, tmp)
            tmp.flush()
            call_command("loaddata", tmp.name)

#python3 manage.py load_ex10 ex10/ressources/ex10_initial_data.json