from faker import Faker
from random import sample, randint

from src.classes.game import Game
from src.classes.player import Player
from src.classes.sql_script import SQLScript
from src.classes.sql_statement import SQLDeleteStatement

PLAYERS_COUNT = 30
GAMES_COUNT = 2 * PLAYERS_COUNT


def main():
    fake = Faker()
    players = [Player(i + 1, fake.first_name(), fake.last_name()) for i in range(PLAYERS_COUNT)]

    script = SQLScript()

    delete_script = SQLScript()
    delete_script.add(SQLDeleteStatement("player__game"))
    delete_script.add(SQLDeleteStatement("player_hand"))
    delete_script.add(SQLDeleteStatement("deck_card"))
    delete_script.add(SQLDeleteStatement("game"))
    delete_script.add(SQLDeleteStatement("player"))
    script.merge(delete_script)

    for i in range(GAMES_COUNT):
        game_players = sample(players, 6)
        default_stack = randint(3, 5) * 500
        small_blind = randint(1, 5) * 5
        game = Game(i + 1, game_players, default_stack, small_blind)
        game.play_game()

        script.merge(game.get_script())

    with open('./out/seed.sql', 'w+') as f:
        f.writelines(script.get_sql())


if __name__ == '__main__':
    main()
