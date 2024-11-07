from enum import Enum
from typing import Any, Dict
import json
import os
from data.pycard_define import CharacterStatusType
from data.pycard_define import EffectType
from utils.draw_text import color_text
from utils.logger import Logger

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建 effect_config.json 文件的绝对路径
config_path = os.path.join(current_dir, "effect_config.json")

# 加载 JSON 文件
with open(config_path, "r", encoding="utf-8") as f:
    effect_config = json.load(f)


class BaseEffect:
    def __init__(self, player, card, effect_type, context) -> None:
        """
        初始化效果基类

        :param name: 效果名称
        :param priority: 效果的优先级，默认为 1
        """

        self.effect_type = effect_type
        self.player = player
        self.card = card
        self.logger = Logger(self.player.name)

        # context: 取决于具体卡牌
        self.context = context
        self.amount = context.get("amount", 0)
        self.immediate = context.get("immediate", False)
        self.end = context.get("end", False)
        self.status = context.get("status", None)
        self.status_amount = context.get("status_amount", None) 
        self.layers = context.get("layers", -1)
        self.sub_effects = []

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

        self.status_amount_type = None
        if self.status_amount:
            status_type_upper = self.status_amount.upper()
            if status_type_upper in CharacterStatusType.__members__:
                self.status_amount_type = CharacterStatusType[status_type_upper]
    
    def skip_execute(self, source, target_object) -> bool:
        # 闪避, 撤离 状态下跳过效果结算
        if target_object != source:
            for skip_status in [CharacterStatusType.DODGE, CharacterStatusType.RETREAT]:
                if target_object.character.has_status(skip_status):
                    self.logger.info(
                        f"{source.name_with_color} -> {target_object.name_with_color}: {color_text(self, 'gray')} [*{skip_status.value}*]",
                        show_source=False,
                    )
                    self.logger.decrease_depth()
                    return True
        return False
                
    def execute(self, source: Any, target: Any, context: Any = None) -> bool:
        """
        执行效果的方法

        :param source: 用于执行效果的来源
        :param target: 用于执行效果的目标
        :param context: 执行效果的上下文
        """
        raise NotImplementedError("子类必须实现 execute 方法")

    def mock_execute(self) -> bool:
        return False
    
    def get_colored_str(self, get_color=True) -> str:
        effect_target, _ = self.get_effect_function(self.player, self.player.opponent)
        # 基于数值
        if self.amount:
            effect_str = self.description.format(self.amount)
        # 基于状态层数
        elif self.status_amount_type:
            status = effect_target.character.has_status(self.status_amount_type)
            if get_color:
                layers_value = status.layers if status else 0
                layers_str = color_text(layers_value,"cyan")
            else:
                layers_str = f"'{self.status_amount_type.value}'"
            effect_str = self.description.format(layers_str)
        else:
            print(self.effect_type)
        if self.immediate:
            effect_str += "(立即)"
        if get_color and self.mock_execute():
            effect_str = color_text(effect_str, "green")
        return effect_str
    
    def __str__(self) -> str:
        return self.get_colored_str(get_color=False)
