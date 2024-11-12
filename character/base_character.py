# /character/base_character.py

from data.character import character_library_instance
from data.item import item_library_instance
from typing import Dict, Any, List
from character.status.base_status import CharacterStatus, CharacterStatusType
from character.character_attribute import CharacterAttribute, CharacterAttributeType
from character import character_status_methods
from utils.logger import Logger


class BaseCharacter:
    def __init__(
        self,
        player,
        name: str,
        hp: int,
        ep: int,
        rp: int,
        delay: int,
        hand_limit: int,
        main_weapon,
        sub_weapon,
        items: List[str],
        cards: List[str],
    ):
        """
        初始化角色基类

        :param name: 角色名称
        :param hp: 角色血量
        :param ep: 角色能量
        :param rp: 角色韧性
        :param delay: 角色滞后
        :param hand_limit: 角色手牌上限
        :param items: 道具列表
        :param cards: 卡牌列表
        """
        self.player = player
        self.name = name
        self.hp = CharacterAttribute(self.player, CharacterAttributeType.HP, hp)
        self.ep = CharacterAttribute(self.player, CharacterAttributeType.EP, ep)
        self.rp = CharacterAttribute(self.player, CharacterAttributeType.RP, rp)
        self.delay = CharacterAttribute(self.player, CharacterAttributeType.DELAY, delay, 0)
        self.hand_limit = CharacterAttribute(self.player, CharacterAttributeType.HANDLIMIT, 10, hand_limit)
        self.main_weapon = main_weapon
        self.sub_weapon = sub_weapon
        self.items = items[::]  # 道具列表
        self.cards = cards[::]  # 卡牌列表
        self.statuses = []  # 状态列表
        self.logger = Logger(self.player.name)
        self._init_cards()

    def _init_cards(self):
        self._add_cards_from_source(self.main_weapon)
        self._add_cards_from_source(self.sub_weapon)
        for item in self.items:
            self._add_cards_from_source(item)

    def _add_cards_from_source(self, source_id):
        if source_id:
            item_info = item_library_instance.get_item_info(source_id)
            if item_info:
                self.cards.extend(item_info.get("cards", []))

    def start_round(self):
        self.ep.set_value(self.ep.max_value)
        self.rp.set_value(self.rp.max_value)
        for status in self.statuses:
            status.start_round()
        self.update_status()
        self.delay.set_value(0)

    def start_turn(self):
        self.update_status()
        for attr in [self.hp, self.ep, self.rp, self.delay]:
            attr.set_resist(0)

    def is_alive(self):
        return self.hp.value > 0

    def has_status(self, status_type: CharacterStatusType) -> bool:
        """
        检查角色是否具有特定的状态

        :param status_type: 要检查的状态类型
        :return: 如果角色具有该状态，返回 True; 否则返回 False
        """
        for status in self.statuses:
            if status.status_type == status_type:
                return status
        return None

    def evaluate_and_update_status(self):
        """
        根据角色的属性更新状态列表
        """
        self.check_death_status()
        self.check_break_status()

    def check_death_status(self):
        character_status_methods.check_death_status(self)

    def check_break_status(self):
        character_status_methods.check_break_status(self)

    def check_flaws_status(self):
        character_status_methods.check_flaws_status(self)

    def append_status(self, status_type_str, context=None):
        character_status_methods.append_status(self, status_type_str, context)

    def reduce_status(self, status_type_str, layers=None):
        character_status_methods.reduce_status(self, status_type_str, layers)

    def update_status(self):
        character_status_methods.update_status(self)

    def detonate_status(self, status_type_str, effect_target="target", sub_effects=[]):
        character_status_methods.detonate_status(self, status_type_str, effect_target, sub_effects)

    @classmethod
    def from_json(cls, player, json_data) -> "BaseCharacter":
        """
        从 JSON 数据创建角色实例

        :param json_data: JSON 数据字典
        :return: BaseCharacter 实例
        """
        try:
            name = json_data["name"]
            hp = json_data["hp"]
            ep = json_data["ep"]
            rp = json_data["rp"]
            delay = json_data["delay"]
            hand_limit = json_data["hand_limit"]
            items = json_data.get("items", [])
            cards = json_data.get("cards", [])
            main_weapon = json_data.get("main_weapon")
            sub_weapon = json_data.get("sub_weapon")
            return cls(player, name, hp, ep, rp, delay, hand_limit, main_weapon, sub_weapon, items, cards)
        except KeyError as e:
            raise ValueError(f"Missing key in JSON data: {e}")

    def __str__(self) -> str:
        return f"{self.name}\t {', '.join(str(attr) for attr in [self.hp, self.ep, self.rp, self.delay])}"

    def display_character_info(self):
        attr_values = ', '.join(f"{attr.name}:{attr.max_value}" for attr in [self.hp, self.ep, self.rp, self.delay])
        return f"{self.name}\t {attr_values}, {self.hand_limit.name}:{self.hand_limit.value}"


if __name__ == "__main__":
    character_info = character_library_instance.get_character_info("ch00001")
    print(character_info)
    character = BaseCharacter.from_json(character_info)
    print(character)
