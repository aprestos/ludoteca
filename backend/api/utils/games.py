from background_task import background

from backend.api.models import BggGame
from backend.api.utils.utils import BoardGameGeek


@background
def update_games():
    # lookup user by id and send them a message
    games = BggGame.objects.all()
    for game in games:
        latest = BoardGameGeek.get_external_game(bgg_id=game.bggid)
        game = BoardGameGeek.convert_external_game(latest, game)
        game.save()
