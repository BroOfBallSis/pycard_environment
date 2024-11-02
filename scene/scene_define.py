from enum import Enum


class BattlePhase(Enum):
    INITIALIZATION = "initialization"
    PLAY_PHASE = "出 牌 阶 段"
    RESOLVE_PHASE = "结 算 阶 段"
    END_TURN = "end_turn"
    DISCARD_PHASE = "弃 牌 阶 段"
    CONCLUDE = "conclude"
