from character.status.base_status import CharacterStatus
from data.pycard_define import CharacterStatusType


def check_death_status(character):
    character.logger.increase_depth()
    """检查角色是否死亡并更新状态"""
    if character.hp.value <= 0 and not character.has_status(CharacterStatusType.DEAD):
        status = CharacterStatus(character.player, CharacterStatusType.DEAD, {"layers": -1})
        character.statuses.append(status)
        character.logger.info(f"获得 {status}")
    character.logger.decrease_depth()


def check_break_status(character):
    character.logger.increase_depth()
    """检查角色是否打断并更新状态"""
    if (
        character.rp.value <= 0
        and not character.has_status(CharacterStatusType.BREAK)
        and not character.has_status(CharacterStatusType.DEAD)
    ):
        status = CharacterStatus(character.player, CharacterStatusType.BREAK, {"layers": -1})
        character.statuses.append(status)
        character.logger.info(f"获得 {status}")
    character.logger.decrease_depth()


def check_flaws_status(character):
    character.logger.increase_depth()
    """检查角色是否破绽并更新状态"""
    if character.delay.value >= character.delay.max_value and not character.has_status(CharacterStatusType.FLAWS):
        status = CharacterStatus(character.player, CharacterStatusType.FLAWS, {"layers": 1})
        character.statuses.append(status)
        character.logger.info(f"获得 {status}")
        character.logger.increase_depth()
        character.logger.info(f"清空 延迟")
        character.delay.set_value(0)
        character.logger.decrease_depth()
    character.logger.decrease_depth()


def update_status(character):
    # 通常在每回合结束调用
    # 触发每个状态
    to_remove_statuses = []
    for status in character.statuses:
        if status.layers > 0:
            status.on_trigger()
        if status.layers <= 0:
            character.logger.increase_depth()
            to_remove_statuses.append(status)
            character.logger.info(f"移除 {status}")
            status.on_remove()
            character.logger.decrease_depth()

    for status in to_remove_statuses:
        character.statuses.remove(status)


def append_status(character, status_type_str, context):
    # 通常由卡牌效果调用
    status_type_upper = status_type_str.upper()
    layers = context.get("layers", None)
    if layers is None:
        layers = 1

    if status_type_upper in CharacterStatusType.__members__:
        status_type = CharacterStatusType[status_type_upper]
        status = character.has_status(status_type)
        if status and status_type != CharacterStatusType.BUFF:
            status.increase(layers)
        else:
            status = CharacterStatus(character.player, status_type, context)
            character.statuses.append(status)
            character.logger.increase_depth()
            character.logger.info(f"获得 {status}")
            character.logger.decrease_depth()


def reduce_status(character, status_type_str, layers):
    # 通常由卡牌效果调用
    status_type_upper = status_type_str.upper()
    if layers is None:
        layers = 1

    if status_type_upper in CharacterStatusType.__members__:
        status_type = CharacterStatusType[status_type_upper]
        status = character.has_status(status_type)
        status.decrease(layers)


def detonate_status(character, status_type_str, effect_target, sub_effects):
    # 通常由卡牌效果调用
    status_type_upper = status_type_str.upper()
    if status_type_upper in CharacterStatusType.__members__:
        status_type = CharacterStatusType[status_type_upper]
        to_remove_status = None
        for status in character.statuses:
            if status.status_type == status_type:
                to_remove_status = status
                for _ in range(status.layers):
                    status.on_trigger()
                    for sub_effect in sub_effects:
                        source = character.player.opponent if effect_target == "target" else character.player
                        sub_effect.execute(source, source.opponent)

        if to_remove_status:
            character.logger.increase_depth()
            character.logger.info(f"移除 {to_remove_status}")
            to_remove_status.on_remove()
            character.statuses.remove(to_remove_status)
            character.logger.decrease_depth()
