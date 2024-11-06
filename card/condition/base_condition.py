from enum import Enum
from card.effect.effect import Effect
from data.pycard_define import CardType, ConditionType
from character.status.base_status import CharacterStatusType
from typing import Any, List, Dict
from utils.draw_text import color_text
from utils.logger import Logger


class BaseCondition:
    def __init__(self, player, card, condition_type: ConditionType, effects: List[Effect]) -> None:
        self.condition_type = condition_type
        self.effects = effects
        self.card = card
        self.player = player
        self.logger = Logger(self.player.name)

    def is_met(self, source: Any, target: Any, context: Any) -> bool:
        """
        检查条件是否满足

        :param source: 来源对象
        :param target: 目标对象
        :param context: 上下文信息
        :return: 是否满足条件
        """
        raise NotImplementedError("子类必须实现 is_met 方法")

    def mock_is_met(self, source: Any, target: Any, context: Any) -> bool:
        return False

    def execute_effects(self, source: Any, target: Any, context: Any) -> None:
        """
        执行效果

        :param source: 来源对象
        :param target: 目标对象
        :param context: 上下文信息
        """
        resolve_priority = context.get("priority", 1)
        resolve_immediate = context.get("immediate", False)
        resolve_end = context.get("end", False)
        for effect in self.effects:
            if (
                resolve_priority == effect.priority
                and resolve_immediate == effect.immediate
                and resolve_end == effect.end
            ):
                # 效果结算被打断的情况
                if source.character.has_status(CharacterStatusType.BREAK):
                    self.logger.increase_depth()
                    self.logger.info(f"{effect.get_colored_str()} [*{CharacterStatusType.BREAK.value}*]")
                    self.logger.decrease_depth()
                    continue
                effect.execute(source, target, context)

    def get_colored_str(self, get_color=True) -> str:
        if get_color:
            effects_str = ", ".join(effect.get_colored_str() for effect in self.effects)
        else:
            effects_str = ", ".join(str(effect) for effect in self.effects)
        condition_type_name = self.condition_type.value

        if condition_type_name:
            full_description = f"{condition_type_name}:{effects_str};"
            # 若条件满足
            if get_color and self.mock_is_met(self.player, self.player.opponent, {}):
                full_description = color_text(full_description, "green")
        else:
            full_description = f"{effects_str};"
        return full_description

    def __str__(self) -> str:
        return self.get_colored_str(get_color=False)


class ConditionFactory:
    @staticmethod
    def create_condition(player, card, condition_type: str, effects: List[Effect]) -> BaseCondition:
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
        raise ValueError(f"Unsupported condition type: {condition_type}")


class ConstantCondition(BaseCondition):
    def is_met(self, source: Any, target: Any, context: Any) -> bool:
        return self.condition_type == ConditionType.TRUE


class TimedCondition(BaseCondition):
    def is_met(self, source: Any, target: Any, context: Any) -> bool:
        source_card_time_cost = source.current_card.time_cost.real_value
        target_card_time_cost = target.current_card.time_cost.real_value

        condition_checks = {
            ConditionType.FIRST: source_card_time_cost < target_card_time_cost,
            ConditionType.SIMULTANEOUS: source_card_time_cost == target_card_time_cost,
            ConditionType.LAST: source_card_time_cost > target_card_time_cost,
        }

        return condition_checks.get(self.condition_type, False)


class TypeConversionCondition(BaseCondition):
    def is_met(self, source: Any, target: Any, context: Any) -> bool:
        posture = source.posture
        current_card = source.current_card

        condition_checks = {
            ConditionType.SWITCH: posture != CardType.NONE and posture != current_card.card_type,
            ConditionType.MAINTAIN: posture != CardType.NONE and posture == current_card.card_type,
            ConditionType.START: posture == CardType.NONE,
            ConditionType.OPPONENT_SWITCH: target.posture != CardType.NONE
            and target.posture != target.current_card.card_type,
        }

        return condition_checks.get(self.condition_type, False)

    def mock_is_met(self, source: Any, target: Any, context: Any) -> bool:
        posture = source.posture
        current_card = self.card
        condition_checks = {
            ConditionType.SWITCH: posture != CardType.NONE and posture != current_card.card_type,
            ConditionType.MAINTAIN: posture != CardType.NONE and posture == current_card.card_type,
            ConditionType.START: posture == CardType.NONE,
            ConditionType.OPPONENT_SWITCH: False,
        }

        return condition_checks.get(self.condition_type, False)
