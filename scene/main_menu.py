from utils.draw_text import color_text, clear_terminal
from card.base_card import BaseCard
from player.base_player import BasePlayer
from data.character import character_library_instance
from data.pycard_define import card_type_color_mapping


class MenuItem:
    def __init__(self, text, action, *args, **kwargs):
        self.text = text
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def execute(self, game):
        if isinstance(self.action, str):
            return game.navigate_to(self.action, *self.args, **self.kwargs)
        else:
            return self.action(*self.args, **self.kwargs)


class Menu:
    def __init__(self, name, title, items):
        self.name = name
        self.title = title
        self.items = items

    def display(self, game):
        print(f"\n{self.title}:")
        for index, item in enumerate(self.items, start=1):
            print(f"{color_text(f'[{index}]','green')} {item.text}")
        choice = input("\n请输入你的选择: ")
        return self.handle_choice(choice, game)

    def handle_choice(self, choice, game):
        if choice.isdigit() and 1 <= int(choice) <= len(self.items):
            clear_terminal()
            return self.items[int(choice) - 1].execute(game)
        else:
            print("无效的选择，请重新输入。")
            return self.display(game)


class CharacterMenu(Menu):
    def __init__(self, name, title, items, player_index):
        super().__init__(name, title, items)
        self.player_index = player_index

    def display(self, game):
        player_color = "blue" if self.player_index == 0 else "red"
        player = color_text(game.players[self.player_index], player_color)
        character_data = character_library_instance.character_data
        public_character = (
            ["ch00001", "ch00002", "ch00003", "ch00004", "ch00005"]
            if self.player_index == 0
            else ["ch00001", "ch00002"]
        )

        while True:
            character = game.characters[self.player_index]
            print(f"\n请选择 {player} 角色, 当前选择 '{color_text(character_data[character]['name'],'green')}':")
            print(
                f"{color_text('[y]','green')} 确 认\t{color_text('[n]','green')} 取 消\t{color_text('[i]','green')} 信 息"
            )
            self.display_character_options(public_character, character_data, character, player_color)
            user_input = input("\n请输入指令: ")
            if not self.handle_user_input(user_input, game, public_character, character_data):
                break

    def display_character_options(self, public_character, character_data, current_character, player_color):
        character_str = ""
        for index, character_id in enumerate(public_character, start=1):
            character_name = character_data[character_id]["name"]
            if character_id == current_character:
                character_name = color_text(f"> {character_name} <", player_color)
            character_str += f"{color_text(f'[{index}]','green')} {character_name}\t"
        print(character_str)

    def handle_user_input(self, user_input, game, public_character, character_data):
        try:
            if user_input.lower() == "y":
                clear_terminal()
                self.items[0].execute(game)
                return False
            elif user_input.lower() == "n":
                clear_terminal()
                self.items[1].execute(game)
                return False
            elif user_input.lower() == "i":
                clear_terminal()
                self.display_character_info(game.characters[self.player_index])
            else:
                character_index = int(user_input) - 1
                if 0 <= character_index < len(public_character):
                    game.characters[self.player_index] = public_character[character_index]
                    clear_terminal()
                else:
                    print(
                        color_text(
                            f"\t{character_index+1} 不在合法范围内([1 ~ {len(public_character)}]), 请重新输入", "yellow"
                        )
                    )
        except ValueError:
            print(color_text(f"\t无效的索引, 请重新输入", "yellow"))
        return True

    def display_character_info(self, character_id):
        # 根据 character_id 加载角色
        player = BasePlayer("player1", 1, character_id, "base", self)
        player.opponent = player
        print(player.character.display_character_info())
        print("牌 组:")
        same_card = []
        for card_id in player.character.cards:
            if card_id not in same_card:
                card = BaseCard.from_json(player, card_id)
                card_color = card_type_color_mapping[card.card_type.value]
                print(color_text(card, card_color))
            same_card.append(card_id)


menu_dict = {
    "main_menu": Menu(
        "main_menu", "主菜单", [MenuItem("进入教程", "tutorial_menu"), MenuItem("对战AI", "pve_player_menu")]
    ),
    "tutorial_menu": Menu(
        "tutorial_menu",
        "教程菜单",
        [
            MenuItem("时间与韧性, 打断与破绽", "time_and_resilience_tutorial"),
            MenuItem("先手与切换, 闪避与撤离", "dodge_and_retreat_tutorial"),
            MenuItem("返回主菜单", "main_menu"),
        ],
    ),
    "pve_player_menu": CharacterMenu(
        "pve_player_menu",
        "选择玩家角色",
        [MenuItem("确认选择", "pve_enemy_menu"), MenuItem("返回主菜单", "main_menu")],
        0,
    ),
    "pve_enemy_menu": CharacterMenu(
        "pve_enemy_menu",
        "选择对手角色",
        [MenuItem("确认选择", "start_battle"), MenuItem("返回上一级", "pve_player_menu")],
        1,
    ),
}
