from character.base_character import BaseCharacter
from card.base_card import BaseCard
from data.character import character_library_instance


class CharacterManager:
    def __init__(self) -> None:
        pass

    def display_character_info(self, character_id):
        # 根据 character_id 加载角色
        character = BaseCharacter.from_json(self, character_library_instance.get_character_info(character_id))
        print(character)
        for card_id in character.cards:
            print(BaseCard.from_json(self.player, card_id))
