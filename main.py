from game import Game
from player import Player


def main():
    names = [
        ("John", "Doe"),
        ("Jack", "Crane"),
        ("Marie", "Curie"),
        ("Oliver", "Twist"),
        ("Evelyn", "Waugh"),
    ]

    players = [Player(i + 1, *name) for i, name in enumerate(names)]

    game = Game(1, players, 1000, 5)
    game.play_game()

    statements = """DELETE FROM player__game;
DELETE FROM history;
DELETE FROM player_hand;
DELETE FROM deck_card;
DELETE FROM game;
DELETE FROM player;
"""
    statements += '\n'.join(list(map(lambda p: p.get_sql(), players)))
    statements += "\n" + game.get_sql()

    with open('seed.sql', 'w+') as f:
        f.writelines(statements)


if __name__ == '__main__':
    main()
