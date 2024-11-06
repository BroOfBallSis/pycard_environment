from card.effect.effect import Effect
from data.pycard_define import CardType, ConditionType, EffectType
from typing import Any, List, Dict
from card.condition.base_condition import BaseCondition
from card.condition.normal_condition import ConstantCondition, TimedCondition, TypeConversionCondition
from card.condition.pay_condition import PayCondition


class ConditionFactory:
    @staticmethod
    def create_condition(player, card, condition_type: str, effects: List[Effect], condition_context) -> BaseCondition:
        """
        创建条件实例的工厂方法

        :param condition_type: 条件类型（字符串）
        :param effects: 关联的效果列表
        :return: BaseCondition 实例
        """
        # 将 condition_type 转换为大写，以便与枚举类型匹配
        condition_type_upper = condition_type.upper()

        if condition_type_upper in ConditionType.__members__:
            condition_enum = ConditionType[condition_type_upper]
            if condition_enum in [ConditionType.TRUE, ConditionType.FALSE]:
                return ConstantCondition(player, card, condition_enum, effects)
            elif condition_enum in [ConditionType.FIRST, ConditionType.SIMULTANEOUS, ConditionType.LAST]:
                return TimedCondition(player, card, condition_enum, effects)
            elif condition_enum in [
                ConditionType.SWITCH,
                ConditionType.MAINTAIN,
                ConditionType.START,
                ConditionType.OPPONENT_SWITCH,
            ]:
                return TypeConversionCondition(player, card, condition_enum, effects)
            elif condition_enum in [ConditionType.PAY_MANA]:
                return PayCondition(player, card, condition_enum, effects, condition_context)
        raise ValueError(f"Unsupported condition type: {condition_type}")


class EffectFactory:
    @staticmethod
    def create_effect(player, card, effect_type_str: str, context: Dict[str, Any]):
        """
        创建效果实例的工厂方法

        :param effect_type: 效果类型
        :param context: 效果上下文，包含必要的参数
        :return: Effect 实例
        """
        # 将 effect_type 转换为大写，以便与枚举类型匹配
        effect_type_upper = effect_type_str.upper()

        if effect_type_upper in EffectType.__members__:
            effect_type = EffectType[effect_type_upper]
            return Effect(player, card, effect_type, context)
        raise ValueError(f"Unsupported effect type: {effect_type_str}")
