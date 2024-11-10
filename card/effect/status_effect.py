from enum import Enum
from typing import Any, Dict
import json
import os
from data.pycard_define import EffectType, CardType, CharacterStatusType
from utils.draw_text import color_text
from utils.logger import Logger
from card.effect.base_effect import effect_config, BaseEffect


class StatusEffect(BaseEffect):
    def get_effect_function(self, source, target):
        effect_target = source if self.effect_target == "source" else target
        effect_function = getattr(effect_target.character, self.effect_function, None)
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
            if self.effect_type in [EffectType.DETONATE_STATUS, EffectType.ACTIVATE_STATUS]:
                effect_function(self.status, self.effect_target, self.sub_effects)
            elif self.effect_type in [
                EffectType.GAIN_STATUS,
                EffectType.GAIN_BUFF,
                EffectType.GAIN_SINGLETON_STATUS,
                EffectType.CAUSE_STATUS,
            ]:
                context = {
                    "amount": self.amount,
                    "layers": self.layers,
                    "buff_posture": self.buff_posture,
                    "buff_effect": self.buff_effect,
                }
                effect_function(self.status, context)
            else:
                effect_function(self.status, self.layers)
        else:
            raise ValueError(f"Does not have function {effect_function}")

        self.logger.decrease_depth()
        return True

    def mock_execute(self) -> bool:
        config = effect_config.get(self.effect_type.value)
        if not config:
            print(f"Invalid effect type: {self.effect_type}")
            return False

        effect_target, _ = self.get_effect_function(self.player, self.player.opponent)
        if self.effect_type == EffectType.DETONATE_STATUS:
            if effect_target.character.has_status(self.status_type):
                return True
        return False

    def get_colored_str(self, get_color=True) -> str:
        effect_target, _ = self.get_effect_function(self.player, self.player.opponent)

        # 状态字符串初始化
        effect_str = ""

        # 状态处理
        if self.effect_type in [EffectType.DETONATE_STATUS, EffectType.GAIN_SINGLETON_STATUS]:
            effect_str = self.description.format(self.status_type.value)

        # 获得或减少状态
        elif self.effect_type in [EffectType.GAIN_STATUS, EffectType.REDUCE_STATUS, EffectType.CAUSE_STATUS]:
            unit = "点" if self.status_type in [CharacterStatusType.MANA] else "层"
            effect_str = self.description.format(self.layers, unit, self.status_type.value)

        # 获得增益: "获得{}层增益:'{}'{}"
        elif self.effect_type in [EffectType.GAIN_BUFF]:
            buff_posture_str = CardType[self.buff_posture.upper()].value
            buff_effect = effect_config.get(self.buff_effect)
            buff_effect_str = buff_effect["description"].format(self.amount)
            effect_str = self.description.format(self.layers, buff_posture_str, buff_effect_str)

        # 激活状态
        elif self.effect_type == EffectType.ACTIVATE_STATUS:
            status = effect_target.character.has_status(self.status_type)
            layers_value = status.layers if status else None

            if get_color:
                layers_str = color_text(layers_value or "X", "cyan" if layers_value else "gray")
            else:
                layers_str = layers_value if layers_value else "X"

            effect_str = self.description.format(layers_str, "点", self.status_type.value)

        # 处理子效果
        if self.sub_effects:
            sub_effect_str = ", ".join(str(sub_effect) for sub_effect in self.sub_effects)
            effect_str += sub_effect_str

        # 处理立即效果标记
        if self.immediate:
            effect_str += "(立即)"

        # 处理颜色
        if get_color and self.mock_execute():
            effect_str = color_text(effect_str, "green")

        return effect_str
