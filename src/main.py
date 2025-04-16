from game import Game
from player import Player
from faker import Faker
from random import sample, randint

PLAYERS_COUNT = 30
GAMES_COUNT = 2 * PLAYERS_COUNT


def main():
    fake = Faker()
    players = [Player(i + 1, fake.first_name(), fake.last_name()) for i in range(PLAYERS_COUNT)]

    statements = """DELETE FROM player__game;
DELETE FROM history;
DELETE FROM player_hand;
DELETE FROM deck_card;
DELETE FROM game;
DELETE FROM player;
"""
    statements += '\n'.join(list(map(lambda p: p.get_sql(), players)))

    for i in range(GAMES_COUNT):
        game_players = sample(players, 6)
        default_stack = randint(3, 5) * 500
        small_blind = randint(1, 5) * 5
        game = Game(i + 1, game_players, default_stack, small_blind)
        game.play_game()

        statements += "\n" + game.get_sql()

    with open('./out/seed.sql', 'w+') as f:
        f.writelines(statements)


if __name__ == '__main__':
    main()
