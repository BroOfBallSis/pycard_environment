from typing import Dict, Any, List
from card.card_define import CardType
from card.condition.base_condition import ConditionFactory, BaseCondition
from card.effect.effect import EffectFactory
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
        card = cls(player, card_id, name, card_type, is_base, consumable, ep_cost, time_cost, [])

        # 解析 conditions
        for cond in json_data["conditions"]:
            condition_type = cond["condition_type"]
            effects_data = cond["effects"]

            # 使用效果工厂创建效果实例
            effects = []
            for effect_data in effects_data:
                effect_type = effect_data["effect_type"]
                effect_param_list = ["amount", "immediate", "status", "layers", "sub_effect"]
                context = {key: effect_data[key] for key in effect_param_list if key in effect_data}
                effect = EffectFactory.create_effect(player, card, effect_type, context)
                effects.append(effect)

                # 使用效果工厂创建子效果实例
                sub_effect = context.get("sub_effect", None)
                if sub_effect:
                    sub_effect_type = sub_effect["effect_type"]
                    sub_context = {key: sub_effect[key] for key in effect_param_list if key in sub_effect}
                    effect.sub_effect = EffectFactory.create_effect(player, card, sub_effect_type, sub_context)

            # 使用条件工厂创建条件实例
            condition = ConditionFactory.create_condition(player, card, condition_type, effects)
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

    def __str__(self) -> str:
        # 控制字段宽度
        name_str = center_text(self.name, 12)  # 假设总宽度为12个字符
        card_type_str = center_text(f"{self.card_type.value}", 4)
        ep_cost_str = center_text(f"{self.ep_cost}", 4)
        time_cost_str = center_text(f"{self.time_cost}", 4)

        conditions_str = " ".join(str(condition) for condition in self.conditions)
        addition_str = ""
        if self.is_base:
            addition_str += " 基础 "
        if self.consumable:
            addition_str += " 消耗 "
        return f"{name_str} ({card_type_str} 体力:{ep_cost_str} 时间:{time_cost_str}{addition_str})  {conditions_str}"
