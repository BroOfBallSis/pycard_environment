from enum import Enum


class CharacterAttributeType(Enum):
    HP = "生命"
    EP = "体力"
    RP = "韧性"
    DELAY = "延迟"
    HANDLIMIT = "手牌上限"


class CharacterStatusType(Enum):
    DEAD = "死亡"
    BREAK = "打断"
    WITHDRAW = "撤离"
    SLOW = "缓慢"
    WEAKNESS = "虚弱"
    VULNERABLE = "易伤"
    DODGE = "闪避"
    POISONED = "中毒"
    BLEEDING = "流血"
    DULL = "迟钝"
    FLAWS = "破绽"
