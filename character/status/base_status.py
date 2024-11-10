# /status/base_status.py
from data.pycard_define import CharacterStatusType, CardType
from card.card_factory import EffectFactory, ConditionFactory
from card.effect.base_effect import effect_config
from utils.logger import Logger


class CharacterStatus:
    def __init__(self, player, status_type: CharacterStatusType, context):
        """
        初始化角色状态

        :param status_type: 状态类型
        :param value: 状态值
        """
        self.player = player
        self.status_type = status_type
        self.amount = context.get("amount", 0)
        self.layers = context.get("layers", -1)
        self.buff_posture = context.get("buff_posture", None)
        self.buff_effect = context.get("buff_effect", None)
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

    def on_resolve(self):
        self.logger.increase_depth()
        """当状态被触发时调用"""
        if self.status_type == CharacterStatusType.BUFF:
            card = self.player.current_card
            buff_posture = CardType[self.buff_posture.upper()]
            if card.card_type == buff_posture:
                context = {"amount": self.amount}
                buff_effect = EffectFactory.create_effect(
                    self.player, self.player.current_card, self.buff_effect, context
                )
                self.player.current_card.temporary_condition.effects.append(buff_effect)
                buff_effect = effect_config.get(self.buff_effect)
                buff_effect_str = buff_effect["description"].format(self.amount)
                self.logger.info(f"打出'{buff_posture.value}', 额外{buff_effect_str}")
            else:
                self.logger.info(f"条件不满足: 打出'{buff_posture.value}'")
            self.decrease(1)
        self.logger.decrease_depth()

    def __str__(self) -> str:
        if self.status_type == CharacterStatusType.BUFF:
            buff_posture_str = CardType[self.buff_posture.upper()].value
            buff_effect = effect_config.get(self.buff_effect)
            buff_effect_str = buff_effect["description"].format(self.amount)
            return f"打出'{buff_posture_str}', 额外{buff_effect_str}({self.layers})"
        if self.layers >= 0:
            return f"{self.status_type.value}({self.layers})"
        else:
            return f"{self.status_type.value}"
