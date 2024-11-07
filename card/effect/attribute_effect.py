from enum import Enum
from typing import Any, Dict
import json
import os
from data.pycard_define import CharacterStatusType
from data.pycard_define import EffectType
from utils.draw_text import color_text
from utils.logger import Logger
from card.effect.base_effect import effect_config, BaseEffect


class AttributeEffect(BaseEffect):
    def get_effect_function(self, source, target):
        effect_target = source if self.effect_target == "source" else target
        effect_attribute = getattr(effect_target.character, self.effect_attribute, None)
        effect_function = getattr(effect_attribute, self.effect_function, None)
        return (effect_target, effect_function)

    def execute(self, source: Any, target: Any, context: Any = None) -> bool:
        """
        执行效果的方法

        :param source: 用于执行效果的来源
        :param target: 用于执行效果的目标
        :param context: 执行效果的上下文
        """
        # 获取效果配置
        config = effect_config.get(self.effect_type.value)
        if not config:
            print(f"Invalid effect type: {self.effect_type}")
            return

        self.logger.increase_depth()
        effect_target, effect_function = self.get_effect_function(source, target)

        # 闪避, 撤离 状态下跳过效果结算
        if self.skip_execute(source, effect_target):
            return False
        self.logger.info(f"{source.name_with_color} -> {effect_target.name_with_color}: {self}", show_source=False)

        if effect_function:
            if self.amount:
                effect_function(self.amount)
            elif self.status_amount_type:
                status = effect_target.character.has_status(self.status_amount_type)
                effect_function(status.layers)
        else:
            raise ValueError(f"Does not have function {effect_function}")

        self.logger.decrease_depth()
        return True
