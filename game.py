from typing import List
from random import choices

from action import Action
from card import Card
from deck import Deck
from player import Player


class Game:
    players: List[Player] = None
    archived_players: List[Player] = []
    cards: List[Card] = []
    deck: Deck = None

    default_stack: int = None
    small_blind: int = None
    round_num: int = None

    current_bet: int = None
    pot: int = None

    last_player: Player = None

    def __init__(self, players: List[Player], default_stack: int, small_blind: int):
        self.players = players
        self.archived_players = []

        for player in players:
            player.game = self

        self.default_stack = default_stack
        self.small_blind = small_blind

        self.deck = Deck()
        self.distribute_players_cards()
        self.distribute_community_cards()

        self.current_bet = 0
        self.round_num = 0
        self.pot = 0

    def distribute_players_cards(self):
        for player in self.players:
            player.hand = [self.deck.cards.pop(0) for _ in range(2)]

    def distribute_community_cards(self):
        self.cards = [self.deck.cards.pop(0) for _ in range(5)]

    def reset_players(self):
        for player in self.players:
            player.stack = self.default_stack
            player.bet = 0
            player.history = []

    def rotate_players(self):
        self.players = self.players[1:] + self.players[:1]

    def play_game(self):
        self.reset_players()

        for _ in range(3):
            self.play_round()
            self.round_num += 1

            for player in self.players:
                self.pot += player.bet
                player.bet = 0

            print("=" * 20)
            print(f"Pot is: {self.pot}")
            self.debug_players()

            if len(self.players) <= 1:
                break

    def play_round(self):
        self.round_num += 1

        for player in self.players[::-1]:
            if player.stack == 0:
                print(f"{player} is out of the game")
                self.players.remove(player)
                self.archived_players.append(player)

        if len(self.players) == 0:
            print("All players are out of the game")
            return

        self.rotate_players()

        self.players[-1].perform_action(Action.SMALL_BLIND)

        while not self.is_turn_finished():
            self.play_turns()

    def is_turn_finished(self):
        not_folded_and_all_in_players = list(filter(lambda p: not p.has_folded() and p.stack != 0, self.players))

        if len(not_folded_and_all_in_players) == 1:
            return True

        for player in not_folded_and_all_in_players:
            if player.bet != self.current_bet:
                return False

        return True

    def play_turns(self):
        for i, player in enumerate(self.players):
            print(f">>> {player} to play")
            if not player.can_play():
                print("Player can't play, skipping")
                continue

            # If no previous player, the current player is the last one
            if not self.last_player:
                print("Didn't find previous player, skipping")
                return

            if self.last_player.id == player.id:
                print("Player is the previous player, skipping")
                return

            if self.last_player.has_folded():
                print("Previous player has folded (1v1), skipping")
                return

            elif self.last_player.has_small_blind():
                player.perform_action(Action.BIG_BLIND)

            elif self.last_player.has_big_blind():
                c = [Action.CHECK, Action.RAISE, Action.FOLD]
                w = [0.7, .15, .15]
                action = choices(c, weights=w, k=1)[0]
                player.perform_action(action)

            elif self.last_player.has_checked():
                c = [Action.ALL_IN, Action.CHECK, Action.RAISE, Action.FOLD]
                w = [0.01, .7, .09, .1]
                action = choices(c, weights=w, k=1)[0]
                player.perform_action(action)

            elif self.last_player.has_raised() or self.last_player.has_called():
                c = [Action.ALL_IN, Action.CALL, Action.RAISE, Action.FOLD]
                w = [0.01, .6, .15, .15]
                action = choices(c, weights=w, k=1)[0]
                player.perform_action(action)

            elif self.last_player.has_all_in():
                c = [Action.ALL_IN, Action.CALL, Action.RAISE, Action.FOLD]
                w = [0.01, .01, .01, .97]
                action = choices(c, weights=w, k=1)[0]
                player.perform_action(action)

            else:
                print("No action performed")

    def debug_players(self):
        print("=" * 20)
        for player in self.players:
            print(player)
        print("=" * 20)

    def __str__(self):
        return ', '.join(list(map(str, self.cards)))
