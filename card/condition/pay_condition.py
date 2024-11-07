from card.condition.base_condition import *


class PayCondition(BaseCondition):
    def __init__(
        self, player, card, condition_type: ConditionType, effects: List[BaseEffect], condition_context=None
    ) -> None:
        super().__init__(player, card, condition_type, effects, condition_context)
        self.amount = condition_context["amount"]
        self.currency = condition_context["currency"]
        self.payed = False
        self.currency_type = None
        status_type_upper = self.currency.upper()
        if status_type_upper in CharacterStatusType.__members__:
            self.currency_type = CharacterStatusType[status_type_upper]

    def reset(self):
        self.payed = False

    def is_met(self, source: Any, target: Any, context: Any) -> bool:
        if self.payed:
            return True

        currency_status = source.character.has_status(self.currency_type)
        if not currency_status or currency_status.layers < self.amount:
            return False
        currency_status.decrease(self.amount)
        self.payed = True
        return True

    def mock_is_met(self, source: Any, target: Any, context: Any) -> bool:
        currency_status = source.character.has_status(self.currency_type)
        return MockResult.TRUE if currency_status and currency_status.layers >= self.amount else MockResult.FALSE

    def get_condition_type_str(self):
        return self.condition_type.value.format(self.amount, self.currency_type.value)
