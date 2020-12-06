import time

import boardgamegeek
import pandas as pd
from boardgamegeek import BGGClient
from django.core.management.base import BaseCommand

from backend.api.models import BggGame, LibraryGame, Player
from backend.api.utils import BggGameUtils

bgg = BGGClient()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file')

    def find(self, query):
        max_count = 10
        while max_count:
            try:
                rs = bgg.search(query)

                if rs:
                    print('Successfully fetch game: ' + rs[0].name + str())
                    return bgg.game(game_id=rs[0].id)

            except boardgamegeek.exceptions.BGGValueError:
                print('[ERROR] Invalid parameters')
                raise

            except boardgamegeek.exceptions.BGGApiRetryError:
                print('[ERROR] Retry after delay, retrying...')
                max_count -= 1
                time.sleep(10)

            except boardgamegeek.exceptions.BGGApiError:
                print('[ERROR] API response invalid or not parsed')
                max_count -= 1
                time.sleep(10)

            except boardgamegeek.exceptions.BGGApiTimeoutError:
                print('[ERROR] Timeout')
                max_count -= 1
                time.sleep(10)

            except Exception as err:
                print('err')
                max_count -= 1
                time.sleep(10)

        raise Exception

    def create_bgg(self, game):
        return BggGameUtils.create(game.id)

    def create_player(self, username):
        player = Player()
        player.username = username
        player.email = username + '@' + 'dumbmail.com'
        player.name = username
        player.save()
        return player

    def add_game(self, bggid, owners):
        for owner in owners:
            self.add_game_to_owner(bggid, owner.strip())

    def add_game_to_owner(self, bggid, owner):
        search = BggGame.objects.filter(bggid=bggid)
        if search.count():
            bgggame = search.first()
        else:

            response = self.find(bggid)

            bgggame = self.create_bgg(response)

        if bgggame:
            playersfilter = Player.objects.filter(username=owner)

            if playersfilter.count():
                player = playersfilter.first()
            else:
                player = self.create_player(owner)

            game = LibraryGame(game=bgggame, owner=player)

            game.game = bgggame

            game.save()
        else:
            print('game not found (' + str(bggid) + ')')

    def handle(self, *args, **options):
        skipped = []
        self.stdout.write(options['file'])
        table = pd.read_csv(options['file'], header=0, delimiter=';')
        for _, row in table.iterrows():
            owners = row['owners'].split(",")
            bggid = row['bggid']
            if bggid:
                try:
                    self.add_game(bggid, owners)
                except Exception as err:
                    # add to skip file
                    skipped.append(str(bggid) + ';' + row['owners'])

            else:
                print('game without id')

        print(skipped)