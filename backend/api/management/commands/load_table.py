from django.core.management.base import BaseCommand, CommandError
from bglibrary.models import BggGame
import pandas as pd


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file")

    def handle(self, *args, **options):
        self.stdout.write(options["file"])
        table = pd.read_csv(options["file"])
        for _, row in table.iterrows():
            if BggGame.objects.filter(bggid=row["id"]).count() == 0:
                g = BggGame(bggid=row["id"], name=row["name"])
                g.save()
