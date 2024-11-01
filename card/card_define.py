from enum import Enum


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
    # 单例状态
    GAIN_SINGLETON_STATUS = "gain_singleton_status"  # 例如：无敌、沉默等

    # 获得状态
    GAIN_STATUS = "gain_status"  # 例如：中毒、增益等
