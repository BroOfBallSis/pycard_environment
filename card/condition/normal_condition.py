from card.condition.base_condition import *


class ConstantCondition(BaseCondition):
    def is_met(self, source: Any, target: Any, context: Any) -> bool:
        return self.condition_type == ConditionType.TRUE


class TimedCondition(BaseCondition):
    def is_met(self, source: Any, target: Any, context: Any) -> bool:
        source_card_time_cost = source.current_card.time_cost.real_value
        target_card_time_cost = target.current_card.time_cost.real_value

        condition_checks = {
            ConditionType.FIRST: source_card_time_cost < target_card_time_cost,
            ConditionType.SIMULTANEOUS: source_card_time_cost == target_card_time_cost,
            ConditionType.LAST: source_card_time_cost > target_card_time_cost,
        }

        return condition_checks.get(self.condition_type, False)


class TypeConversionCondition(BaseCondition):
    def is_met(self, source: Any, target: Any, context: Any) -> bool:
        posture = source.posture
        current_card = source.current_card

        condition_checks = {
            ConditionType.SWITCH: posture != CardType.NONE and posture != current_card.card_type,
            ConditionType.MAINTAIN: posture != CardType.NONE and posture == current_card.card_type,
            ConditionType.START: posture == CardType.NONE,
            ConditionType.OPPONENT_SWITCH: target.posture != CardType.NONE
            and target.posture != target.current_card.card_type,
        }

        return condition_checks.get(self.condition_type, False)

    def mock_is_met(self, source: Any, target: Any, context: Any) -> bool:
        posture = source.posture
        current_card = self.card
        condition_checks = {
            ConditionType.SWITCH: posture != CardType.NONE and posture != current_card.card_type,
            ConditionType.MAINTAIN: posture != CardType.NONE and posture == current_card.card_type,
            ConditionType.START: posture == CardType.NONE,
            ConditionType.OPPONENT_SWITCH: False,
        }

        return condition_checks.get(self.condition_type, False)
