# /status/base_status.py
from data.pycard_define import CharacterStatusType
from utils.logger import Logger


class CharacterStatus:
    def __init__(self, player, status_type: CharacterStatusType, layers: int = 1):
        """
        初始化角色状态

        :param status_type: 状态类型
        :param value: 状态值
        """
        self.player = player
        self.status_type = status_type
        self.layers = layers
        self.logger = Logger(self.player.name)

    def increase(self, amount: int) -> None:
        """增加状态值"""
        self.logger.increase_depth()
        old_value = self.layers
        self.layers += amount
        self.logger.info(f"{self.status_type.value}: {old_value} ↑ {self.layers}")
        self.logger.decrease_depth()

    def decrease(self, amount: int) -> None:
        """减少状态值"""
        self.logger.increase_depth()
        old_value = self.layers
        self.layers -= amount
        self.logger.info(f"{self.status_type.value}: {old_value} ↓ {self.layers}")
        self.logger.decrease_depth()

    def set_value(self, value: int):
        if self.layers < 0:
            # 单例状态无法设置
            pass
        else:
            self.logger.increase_depth()
            old_value = self.layers
            self.layers = value
            self.logger.info(f"{self.status_type.value}: {old_value} → {self.layers}")
            self.logger.decrease_depth()

    def start_round(self):
        if self.status_type == CharacterStatusType.MANA:
            self.set_value(self.layers // 2)
        else:
            self.set_value(0)

    def on_add(self) -> None:
        """当状态首次添加时调用"""
        pass

    def on_remove(self) -> None:
        self.logger.increase_depth()
        """当状态被移除时调用"""
        if self.status_type == CharacterStatusType.BREAK:
            self.logger.info(f"恢复韧性")
            self.player.character.rp.set_value(self.player.character.rp.max_value)
            if self.player.opponent.character.delay.value > 0:
                self.logger.info(f"清空对手延迟")
                self.player.opponent.character.delay.set_value(0)
        self.logger.decrease_depth()

    def on_trigger(self) -> None:
        self.logger.increase_depth()
        """当状态被触发时调用"""
        if self.status_type == CharacterStatusType.SLOW:
            self.logger.info(f"{self}: 增加1点延迟")
            self.player.character.delay.increase(1)
            self.decrease(1)
        self.logger.decrease_depth()

    def __str__(self) -> str:
        if self.layers >= 0:
            return f"{self.status_type.value}({self.layers})"
        else:
            return f"{self.status_type.value}"
