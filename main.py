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

    players = [Player(i, *name) for i, name in enumerate(names)]

    for _ in range(100):
        game = Game(players, 1000, 5)
        game.play_game()


if __name__ == '__main__':
    main()
