from card.condition.base_condition import *


class PayCondition(BaseCondition):
    def __init__(
        self, player, card, condition_type: ConditionType, effects: List[BaseEffect], condition_context=None
    ) -> None:
        super().__init__(player, card, condition_type, effects, condition_context)
        self.amount = condition_context["amount"]
        self.payed = False

    def reset(self):
        self.payed = False

    def is_met(self, source: Any, target: Any, context: Any) -> bool:
        if self.payed:
            return True
        mana_status = source.character.has_status(CharacterStatusType.MANA)
        if not mana_status or mana_status.layers < self.amount:
            return False
        mana_status.decrease(self.amount)
        self.payed = True
        return True

    def mock_is_met(self, source: Any, target: Any, context: Any) -> bool:
        mana_status = source.character.has_status(CharacterStatusType.MANA)
        return MockResult.TRUE if mana_status and mana_status.layers >= self.amount else MockResult.FALSE

    def get_condition_type_str(self):
        return self.condition_type.value.format(self.amount)
