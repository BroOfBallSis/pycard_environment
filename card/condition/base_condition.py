from enum import Enum
from card.effect.effect import Effect
from data.pycard_define import CardType, ConditionType
from character.status.base_status import CharacterStatusType
from typing import Any, List, Dict
from utils.draw_text import color_text
from utils.logger import Logger


class BaseCondition:
    def __init__(
        self, player, card, condition_type: ConditionType, effects: List[Effect], condition_context=None
    ) -> None:
        self.condition_type = condition_type
        self.effects = effects
        self.card = card
        self.player = player
        self.logger = Logger(self.player.name)

    def reset(self):
        pass

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
                skip_effect = False
                # 效果结算被打断的情况
                for skip_status in [CharacterStatusType.BREAK, CharacterStatusType.DEAD]:
                    if source.character.has_status(skip_status):
                        self.logger.increase_depth()
                        self.logger.info(f"{effect} [*{skip_status.value}*]")
                        self.logger.decrease_depth()
                        skip_effect = True
                        break
                if not skip_effect:
                    effect.execute(source, target, context)

    def get_condition_type_str(self):
        return self.condition_type.value

    def get_colored_str(self, get_color=True) -> str:
        if get_color:
            effects_str = ", ".join(effect.get_colored_str() for effect in self.effects)
        else:
            effects_str = ", ".join(str(effect) for effect in self.effects)
        condition_type_str = self.get_condition_type_str()

        if condition_type_str:
            full_description = f"{condition_type_str}:{effects_str};"
            # 若条件满足
            if get_color and self.mock_is_met(self.player, self.player.opponent, {}):
                full_description = color_text(full_description, "green")
        else:
            full_description = f"{effects_str};"
        return full_description

    def __str__(self) -> str:
        return self.get_colored_str(get_color=False)
