from enum import Enum

character_to_policy = {"ch00001": "SWORD_AI", "ch00002": "HAMMER_AI", "th00001": "SWORD_AI"}


class PolicyType(Enum):
    BASE = ("base_policy", "BasePolicy")
    RANDOM = ("random_policy", "RandomPolicy")
    REMOTE = ("remote_policy", "RemotePolicy")
    RL = ("rl_policy", "RLPolicy")
    TERMINAL = ("terminal_policy", "TerminalPolicy")
    SWORD_AI = ("ai_policy.sword_policy", "SwordPolicy")
    HAMMER_AI = ("ai_policy.hammer_policy", "HammerPolicy")


class CardType(Enum):
    NONE = "无"
    WIND = "风"
    FIRE = "火"
    MOUNTAIN = "山"
    FOREST = "林"
    SHADOW = "阴"
    THUNDER = "雷"


class ConditionType(Enum):
    TRUE = ""
    FALSE = "恒假"
    FIRST = "先手"
    SIMULTANEOUS = "同时"
    LAST = "后手"
    SWITCH = "切换"
    MAINTAIN = "保持"
    START = "启动"
    OPPONENT_SWITCH = "识破"
    PAY_MANA = "支付{}点魔力"


class MockResult(Enum):
    FALSE = -1
    UNKNOWN = 0
    TRUE = 1


class EffectType(Enum):
    CAUSE_DAMAGE = "cause_damage"
    CAUSE_STUN = "cause_stun"
    CAUSE_DELAY = "cause_delay"
    RESIST_DAMAGE = "resist_damage"
    RESIST_STUN = "resist_stun"
    RESIST_DELAY = "resist_delay"
    RECOVER_HP = "recover_hp"
    RECOVER_EP = "recover_ep"
    RECOVER_RP = "recover_rp"
    REDUCE_DELAY = "reduce_delay"
    DRAW_CARD = "draw_card"
    GAIN_SINGLETON_STATUS = "gain_singleton_status"  # 单例状态
    GAIN_STATUS = "gain_status"
    REDUCE_STATUS = "reduce_status"
    DETONATE_STATUS = "detonate_status"


class CharacterAttributeType(Enum):
    HP = "生命"
    EP = "体力"
    RP = "韧性"
    DELAY = "延迟"
    HANDLIMIT = "手牌上限"


class CharacterStatusType(Enum):
    DEAD = "死亡"
    BREAK = "打断"
    RETREAT = "撤离"
    SLOW = "缓慢"
    WEAKNESS = "虚弱"
    VULNERABLE = "易伤"
    DODGE = "闪避"
    POISONED = "中毒"
    BLEEDING = "流血"
    DULL = "迟钝"
    FLAWS = "破绽"
    MANA = "魔力"


class BattlePhase(Enum):
    INITIALIZATION = "initialization"
    PLAY_PHASE = "出 牌 阶 段"
    RESOLVE_PHASE = "结 算 阶 段"
    END_TURN = "end_turn"
    DISCARD_PHASE = "弃 牌 阶 段"
    CONCLUDE = "conclude"
