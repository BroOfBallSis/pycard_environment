# /effect/base_effect.py

from enum import Enum
from typing import Any, Dict
import json
import os
from character.character_define import CharacterStatusType
from card.card_define import EffectType
from utils.draw_text import color_text

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建 effect_config.json 文件的绝对路径
config_path = os.path.join(current_dir, "effect_config.json")

# 加载 JSON 文件
with open(config_path, "r") as f:
    effect_config = json.load(f)


class Effect:
    def __init__(self, player, card, effect_type, context) -> None:
        """
        初始化效果基类

        :param name: 效果名称
        :param priority: 效果的优先级，默认为 1
        """

        self.effect_type = effect_type
        self.player = player
        self.card = card

        # context: 取决于具体卡牌
        self.context = context
        self.amount = context.get("amount", 0)
        self.immediate = context.get("immediate", False)
        self.end = context.get("end", False)
        self.status = context.get("status", None)
        self.layers = context.get("layers", -1)

        # config: 取决于效果类型
        config = effect_config.get(self.effect_type.value)
        if not config:
            print(f"Invalid effect type: {self.effect_type}")
            return
        # priority: 0-抵抗, 1-状态, 2-伤害, 3-恢复
        self.priority = config.get("priority", 0)
        self.effect_target = config.get("target", None)
        self.effect_component = config.get("component", None)
        self.effect_attribute = config.get("attribute", None)
        self.effect_function = config.get("function", None)
        self.description = config["description"]

        self.status_type = None
        if self.status:
            status_type_upper = self.status.upper()
            if status_type_upper in CharacterStatusType.__members__:
                self.status_type = CharacterStatusType[status_type_upper]

    def execute(self, source: Any, target: Any, context: Any = None) -> bool:
        """
        执行效果的方法

        :param source: 用于执行效果的来源
        :param target: 用于执行效果的目标
        :param context: 执行效果的上下文
        """
        config = effect_config.get(self.effect_type.value)
        if not config:
            print(f"Invalid effect type: {self.effect_type}")
            return

        target_object = source if self.effect_target == "source" else target
        component_object = getattr(target_object, self.effect_component, None)

        # 闪避, 撤离 状态下跳过效果结算
        if target_object != source:
            if target_object.character.has_status(CharacterStatusType.DODGE):
                print(f"\t{source.name} -> {target_object.name} [{CharacterStatusType.DODGE.value}]: {self}")
                return False
            elif target_object.character.has_status(CharacterStatusType.WITHDRAW):
                print(f"\t{source.name} -> {target_object.name} [{CharacterStatusType.WITHDRAW.value}]: {self}")
                return False
            elif source.character.has_status(CharacterStatusType.DEAD):
                print(f"\t{source.name} [{CharacterStatusType.DEAD.value}]: {self} ")
                return False

        print(f"\t{source.name} -> {target_object.name}: {self}")
        # 状态类效果:组件(角色)->方法
        if self.status:
            function_object = getattr(component_object, self.effect_function, None)
            if function_object:
                function_object(self.status, self.layers)
            else:
                raise ValueError(f"Does not have function {function_object}")
        # 属性类效果:组件 -> 属性 -> 方法
        elif self.effect_attribute:
            attribute_object = getattr(component_object, self.effect_attribute, None)
            function_object = getattr(attribute_object, self.effect_function, None)
            if function_object:
                function_object(self.amount)
            else:
                raise ValueError(f"Does not have function {function_object}")
        # 组件类效果:组件 -> 方法
        else:
            function_object = getattr(component_object, self.effect_function, None)
            if function_object:
                function_object(self.amount)
            else:
                raise ValueError(f"Does not have function {function_object}")
        return True

    def mock_execute(self) -> bool:
        """
        执行效果的方法

        :param source: 用于执行效果的来源
        :param target: 用于执行效果的目标
        :param context: 执行效果的上下文
        """
        config = effect_config.get(self.effect_type.value)
        if not config:
            print(f"Invalid effect type: {self.effect_type}")
            return False

        target_object = self.player if self.effect_target == "source" else self.player.opponent
        component_object = getattr(target_object, self.effect_component, None)

        # 属性类效果:组件 -> 属性 -> 方法
        if self.effect_type in [EffectType.CAUSE_DAMAGE, EffectType.CAUSE_STUN]:
            attribute_object = getattr(component_object, self.effect_attribute, None)
            if self.amount >= attribute_object.value:
                return True
        return False

    def __str__(self) -> str:
        placeholder_count = self.description.count("{}")
        if self.effect_type == EffectType.GAIN_SINGLETON_STATUS:
            effect_str = self.description.format(self.status_type.value)
        elif self.effect_type == EffectType.GAIN_STATUS:
            effect_str = self.description.format(self.layers, self.status_type.value)
        elif placeholder_count == 1:
            effect_str = self.description.format(self.amount)
        else:
            effect_str = self.description  # 如果没有占位符，直接使用描述
        if self.immediate:
            effect_str += "(立即)"
        if self.mock_execute():
            effect_str = color_text(effect_str, "green")
        return effect_str


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
