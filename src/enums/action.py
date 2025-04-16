from enum import Enum


class Action(Enum):
    SMALL_BLIND = "SMALL_BLIND"
    BIG_BLIND = "BIG_BLIND"
    CALL = "CALL"
    CHECK = "CHECK"
    FOLD = "FOLD"
    RAISE = "RAISE"
    ALL_IN = "ALL_IN"
