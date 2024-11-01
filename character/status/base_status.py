# /status/base_status.py
from character.character_define import CharacterStatusType


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
        self.logger = self.player.logger if self.player else None

    def increase(self, amount: int) -> None:
        """增加状态值"""
        self.layers += amount

    def decrease(self, amount: int) -> None:
        """减少状态值"""
        self.layers -= amount

    def on_add(self) -> None:
        """当状态首次添加时调用"""
        pass

    def on_remove(self) -> None:
        """当状态被移除时调用"""
        if self.status_type == CharacterStatusType.BREAK:
            self.player.character.rp.set_value(self.player.character.rp.max_value)
            self.logger.info(f"恢复全部 韧性", 2)
        pass

    def on_trigger(self) -> None:
        """当状态被触发时调用"""
        pass

    def __str__(self) -> str:
        if self.layers > 0:
            return f"{self.status_type.value}({self.layers})"
        else:
            return f"{self.status_type.value}"

    def __str__(self) -> str:
        if self.layers > 0:
            return f"{self.status_type.value}({self.layers})"
        else:
            return f"{self.status_type.value}"
