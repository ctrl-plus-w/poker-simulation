from dataclasses import dataclass
from datetime import datetime
from random import gauss
from typing import Tuple

from src.classes.card import Card
from src.classes.history import History
from src.classes.sql_script import SQLScript
from src.classes.sql_statement import SQLInsertStatement
from src.classes.sql_statement_builder import SQLInsertStatementBuilder
from src.classes.time_generator import time_generator
from src.enums.action import Action

current_hand_id = 1


def gaussian_bet(min_bet, stack):
    max_bet = (stack + min_bet) // 2
    mean = min_bet + (max_bet - min_bet) * 0.3  # Skew the mean toward lower bets
    stddev = (max_bet - min_bet) * 0.2  # Keep most values reasonably low

    bet = int(gauss(mean, stddev))

    # Clamp bet to the valid range
    return max(min_bet, min(bet, max_bet))


@dataclass
class Player:
    id: int = None
    first_name: str = None
    last_name: str = None
    hand: Tuple[Card, Card] = None
    history: list[History] = None
    game: 'Game' = None
    bet: int = 0
    stack: int = 0
    hand_id: int = None
    created_at: datetime = time_generator.now()

    def has_played_action(self, action: Action):
        history_actions = list(filter(lambda a: a.round_num == self.game.round_num, self.history))
        if len(history_actions) == 0:
            return False
        return history_actions[-1].action == action

    def can_play(self):
        if self.stack <= 0:
            return False

        if self.has_folded() or self.has_all_in():
            return False

        return True

    def has_small_blind(self):
        return self.has_played_action(Action.SMALL_BLIND)

    def has_big_blind(self):
        return self.has_played_action(Action.BIG_BLIND)

    def has_checked(self):
        return self.has_played_action(Action.CHECK)

    def has_called(self):
        return self.has_played_action(Action.CALL)

    def has_raised(self):
        return self.has_played_action(Action.RAISE)

    def has_folded(self):
        return self.has_played_action(Action.FOLD)

    def has_all_in(self):
        return self.has_played_action(Action.ALL_IN)

    def perform_bet(self, value: int):
        if value == 0:
            raise Exception("Invalid bet value (0)")
        if value > self.stack:
            raise Exception("Invalid bet value")

        self.bet = value
        self.stack -= value
        self.game.current_bet = max(self.bet, self.game.current_bet)

    def perform_action(self, action: Action):
        print(f"{self} is playing action {action.name}:")

        if action == Action.SMALL_BLIND:
            print(f"  {self.first_name} {self.last_name} is playing small blind")
            self.perform_bet(min(self.game.small_blind, self.stack))
            self.history.append(History(action, self.game.small_blind, self.game.round_num))
            self.game.last_player = self

        if action == Action.BIG_BLIND:
            print(f"  {self.first_name} {self.last_name} is playing big blind")
            self.perform_bet(min(self.game.small_blind * 2, self.stack))
            self.history.append(History(action, self.game.small_blind * 2, self.game.round_num))
            self.game.last_player = self

        if action == Action.FOLD:
            print(f"  {self.first_name} {self.last_name} folded")
            self.history.append(History(action, None, self.game.round_num))

        elif action == Action.CHECK:
            print(f"  {self.first_name} {self.last_name} checked")
            self.history.append(History(action, None, self.game.round_num))
            self.game.last_player = self

        elif action == Action.CALL:
            if self.game.current_bet >= self.game.current_bet:
                return self.perform_action(Action.ALL_IN)
            if self.game.current_bet <= 0:
                raise Exception("Invalid call value")
            print(f"  {self.first_name} {self.last_name} called ({self.game.current_bet})")
            self.perform_bet(self.game.current_bet)
            self.history.append(History(action, self.game.current_bet, self.game.round_num))
            self.game.last_player = self

        elif action == Action.RAISE:
            min_bet = max(self.game.current_bet + 1, 0)
            if min_bet == self.stack:
                return self.perform_action(Action.CALL)
            if min_bet >= self.stack:
                return self.perform_action(Action.ALL_IN)

            value = gaussian_bet(min_bet, self.stack)
            print(f"  {self.first_name} {self.last_name} raised to {value} (current bet: {self.game.current_bet})")
            self.history.append(History(action, value, self.game.round_num))
            self.perform_bet(value)
            self.game.last_player = self

        elif action == Action.ALL_IN:
            value = self.stack
            print(f"  {self.first_name} {self.last_name} went all-in ({value})")
            self.history.append(History(action, value, self.game.round_num))
            self.perform_bet(value)
            self.game.last_player = self

    def get_sql_statement(self):
        builder = SQLInsertStatementBuilder("player", ["id", "first_name", "last_name", "created_at"], )
        return builder.build([self.id, self.first_name, self.last_name, self.created_at])

    def get_game_script(self):
        script = SQLScript()

        script.add(SQLInsertStatement("player__game", ["player_id", "game_id"], [self.id, self.game.id]))

        player_hand_builder = SQLInsertStatementBuilder("player_hand",
                                                        ["id", "player_id", "deck_card_id", "deck_card_id1",
                                                         "created_at"])
        script.add(player_hand_builder.build(
            [self.hand_id, self.id, self.hand[0].id, self.hand[1].id, self.created_at]))

        for history_action in self.history:
            script.add(history_action.get_sql_statement(self, self.game))

        return script

    def __str__(self):
        return f"{self.first_name} {self.last_name} with cards ({self.hand[0]}, {self.hand[1]}) [stack: {self.stack}, bet: {self.bet}]"

    def reset_hand_id(self):
        global current_hand_id
        self.hand_id = current_hand_id
        current_hand_id += 1
