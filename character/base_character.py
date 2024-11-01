# /character/base_character.py

from data.character import character_library_instance
from typing import Dict, Any, List
from character.status.base_status import CharacterStatus, CharacterStatusType
from character.character_attribute import CharacterAttribute, CharacterAttributeType


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
        self.items = items  # 道具列表
        self.cards = cards  # 卡牌列表
        self.statuses = []  # 状态列表
        self.logger = self.player.logger if self.player else None

    def start_round(self):
        self.ep.set_value(self.ep.max_value)
        self.rp.set_value(self.rp.max_value)
        self.statuses = []
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
        """检查角色是否死亡并更新状态"""
        if self.hp.value <= 0 and not self.has_status(CharacterStatusType.DEAD):
            status = CharacterStatus(self.player, CharacterStatusType.DEAD, -1)
            self.statuses.append(status)
            self.logger.info(f"获得 {status}", 2)

    def check_break_status(self):
        """检查角色是否打断并更新状态"""
        if self.rp.value <= 0 and not self.has_status(CharacterStatusType.BREAK):
            status = CharacterStatus(self.player, CharacterStatusType.BREAK, -1)
            self.statuses.append(status)
            self.logger.info(f"获得 {status}", 2)

    def check_flaws_status(self):
        """检查角色是否破绽并更新状态"""
        if self.delay.value >= self.delay.max_value and not self.has_status(CharacterStatusType.FLAWS):
            status = CharacterStatus(self.player, CharacterStatusType.FLAWS, 1)
            self.statuses.append(status)
            self.logger.info(f"获得 {status}", 2)
            self.delay.set_value(0)
            self.logger.info(f"清空 {self.delay.attribute_type.value}", 2)

    def append_status(self, status_type_str, layers=None):
        status_type_upper = status_type_str.upper()
        if layers is None:
            layers = 1

        if status_type_upper in CharacterStatusType.__members__:
            status_type = CharacterStatusType[status_type_upper]
            status = CharacterStatus(self.player, status_type, layers)
            self.statuses.append(status)
            self.logger.info(f"获得 {status}", 2)

    def update_status(self):
        for status in self.statuses:
            if status.layers <= 0:
                self.statuses.remove(status)
                self.logger.info(f"移除 {status}", 2)
                status.on_remove()

    @classmethod
    def from_json(cls, player, json_data: Dict[str, Any]) -> "BaseCharacter":
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
            return cls(player, name, hp, ep, rp, delay, hand_limit, items, cards)
        except KeyError as e:
            raise ValueError(f"Missing key in JSON data: {e}")

    def __str__(self) -> str:
        return f"{self.name}\t {', '.join(str(attr) for attr in [self.hp, self.ep, self.rp, self.delay])}"


if __name__ == "__main__":
    character_info = character_library_instance.get_character_info("ch00001")
    print(character_info)
    character = BaseCharacter.from_json(character_info)
    print(character)
