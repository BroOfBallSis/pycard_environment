from typing import Dict, Any, List
from data.pycard_define import CardType
from card.condition.base_condition import BaseCondition
from card.card_factory import ConditionFactory, EffectFactory
from utils.draw_text import center_text
from card.card_attribute import CardAttribute
from data.card import card_library_instance


class BaseCard:
    def __init__(
        self,
        player,
        card_id: str,
        name: str,
        card_type: CardType,
        is_base: bool,
        consumable: bool,
        temporary: bool,
        ep_cost: int,
        time_cost: int,
        conditions: List[BaseCondition],
    ) -> None:
        self.player = player
        self.card_id = card_id
        self.name = name
        self.card_type = card_type
        self.ep_cost = CardAttribute("体力费用", ep_cost)
        self.time_cost = CardAttribute("时间费用", time_cost)
        self.conditions = conditions
        self.is_base = is_base
        self.consumable = consumable
        self.temporary = temporary

    @classmethod
    def from_json(cls, player, card_id) -> "BaseCard":
        """
        从 JSON 数据创建卡牌实例

        :param json_data: JSON 数据字典
        :return: Card 实例
        """
        json_data = card_library_instance.get_card_info(card_id)
        name = json_data["name"]
        card_type = CardType[json_data["card_type"].upper()]  # 使用枚举
        ep_cost = json_data["ep_cost"]
        time_cost = json_data["time_cost"]
        is_base = json_data.get("is_base", False)
        consumable = json_data.get("consumable", False)
        temporary = json_data.get("temporary", False)
        card = cls(player, card_id, name, card_type, is_base, consumable, temporary, ep_cost, time_cost, [])

        # 解析 conditions
        for cond in json_data["conditions"]:
            condition_type = cond["condition_type"]
            effects_data = cond["effects"]

            # 使用效果工厂创建效果实例
            effects = []
            for effect_data in effects_data:
                effect_type = effect_data["effect_type"]
                effect_param_list = [
                    "amount",
                    "immediate",
                    "status",
                    "layers",
                    "sub_effects",
                    "status_amount",
                    "next_card_id",
                ]
                context = {key: effect_data[key] for key in effect_param_list if key in effect_data}
                effect = EffectFactory.create_effect(player, card, effect_type, context)
                effects.append(effect)

                # 使用效果工厂创建子效果实例
                sub_effects = context.get("sub_effects", [])
                for sub_effect in sub_effects:
                    sub_effects_type = sub_effect["effect_type"]
                    sub_context = {key: sub_effect[key] for key in effect_param_list if key in sub_effect}
                    effect.sub_effects.append(EffectFactory.create_effect(player, card, sub_effects_type, sub_context))

            # 使用条件工厂创建条件实例
            condition_param_list = [
                "amount",
                "immediate",
                "status",
                "layers",
                "sub_condition",
                "status_amount",
                "currency",
            ]
            condition_context = {key: cond[key] for key in condition_param_list if key in cond}
            condition = ConditionFactory.create_condition(player, card, condition_type, effects, condition_context)
            card.conditions.append(condition)
        return card

    def clear_mod(self) -> None:
        self.ep_cost.set_mod(0)
        self.time_cost.set_mod(0)

    def play(self, source: Dict[str, Any], target: Dict[str, Any], context: Any) -> None:
        """
        执行卡牌的效果

        :param source: 来源对象
        :param target: 目标对象
        :param context: 上下文信息
        """
        for condition in self.conditions:
            if condition.is_met(source, target, context):
                condition.execute_effects(source, target, context)

    def get_colored_str(self, get_color=True) -> str:
        # 控制字段宽度
        name_str = center_text(self.name, 12)  # 假设总宽度为12个字符
        card_type_str = center_text(f"{self.card_type.value}", 4)
        ep_cost_str = center_text(f"{self.ep_cost}", 4)
        if get_color:
            time_cost_str = center_text(f"{self.time_cost.get_colored_str()}", 4)
        else:
            time_cost_str = center_text(f"{self.time_cost}", 4)
        if get_color:
            conditions_str = "\n·    ".join(condition.get_colored_str() for condition in self.conditions)
        else:
            conditions_str = "\n·    ".join(str(condition) for condition in self.conditions)
        addition_str = ""
        if self.is_base:
            addition_str += " 基础 "
        if self.consumable:
            addition_str += " 消耗 "
        if self.temporary:
            addition_str += " 临时 "
        return (
            f"{name_str} ({card_type_str} 时间:{time_cost_str} 体力:{ep_cost_str}{addition_str})\n·    {conditions_str}"
        )

    def __str__(self) -> str:
        return self.get_colored_str(get_color=False)
