from data.pycard_define import CharacterAttributeType
from utils.logger import Logger


class CharacterAttribute:
    def __init__(self, player, attribute_type: "CharacterAttributeType", max_value: int, value: int = -1):
        self.player = player
        self.attribute_type = attribute_type
        self.name = attribute_type.value
        self.max_value = max_value
        self.value = max_value if value == -1 else value
        self.resist_value = 0
        self.logger = Logger(self.player.name)

    def increase(self, amount: int):
        self.logger.increase_depth()
        old_value = self.value
        self.value = self.value + amount

        # 延迟 无上限
        if self.attribute_type != CharacterAttributeType.DELAY:
            self.value = min(self.value + amount, self.max_value)

        right_value_str = f"{self.value} (max)" if self.value == self.max_value else f"{self.value}"
        self.logger.info(f"{self.name}: {old_value} ↑ {right_value_str}")

        # 生命 统计增加的值
        if self.attribute_type == CharacterAttributeType.HP:
            if self.attribute_type in self.player.round_info:
                self.player.round_info[self.attribute_type] += amount
            else:
                self.player.round_info[self.attribute_type] = amount

        self.logger.decrease_depth()

    def decrease(self, amount: int):
        self.logger.increase_depth()

        old_value = self.value
        real_amount = amount
        if self.resist_value > 0:
            # amount 受到 self.temp_value 的抵抗，且不小于0
            real_amount = max(amount - self.resist_value, 0)

            # self.temp_value 受到 amount 的削减，且不小于0
            self.resist_value = max(self.resist_value - amount, 0)

            self.logger.info(f"抵抗生效: {amount} ↓ {real_amount}")

        self.value = self.value - real_amount
        self.logger.info(f"{self.name}: {old_value} ↓ {self.value}")

        # 体力, 韧性 的溢出转化
        if self.attribute_type in [CharacterAttributeType.EP, CharacterAttributeType.RP] and self.value < 0:
            self.logger.increase_depth()
            self.logger.info(f"溢出的{self.attribute_type.value}伤害 转化为 缓慢 ")
            layers = -self.player.character.rp.value
            self.set_value(0)
            self.player.character.append_status("slow", layers)
            self.logger.decrease_depth()

        # 回合统计
        if self.attribute_type in self.player.round_info:
            self.player.round_info[self.attribute_type] -= real_amount
        else:
            self.player.round_info[self.attribute_type] = -real_amount

        self.logger.decrease_depth()

    def increase_resist(self, amount: int):
        self.resist_value = self.resist_value + amount

    def decrease_resist(self, amount: int):
        self.resist_value = self.resist_value - amount

    def set_resist(self, value: int):
        self.resist_value = value

    def set_value(self, value: int):
        self.logger.increase_depth()
        old_value = self.value
        self.value = value
        self.logger.info(f"{self.name}: {old_value} → {self.value}")
        self.logger.decrease_depth()

    def __str__(self) -> str:
        return f"{self.name}:{self.value}/{self.max_value}"
