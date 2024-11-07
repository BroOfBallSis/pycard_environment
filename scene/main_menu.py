from utils.draw_text import color_text, clear_terminal


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
    def __init__(self, name, title, items, parent=None):
        self.name = name
        self.title = title
        self.items = items
        self.parent = parent

    def display(self, game):
        print(f"\n{self.title}:")
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item.text}")
        if self.parent:
            print(f"{len(self.items) + 1}. 返回上一级")
        elif self.name != "main_menu":
            print(f"{len(self.items) + 1}. 返回主菜单")
        choice = input("\n请输入你的选择: ")
        return self.handle_choice(choice, game)

    def handle_choice(self, choice, game):
        if choice.isdigit() and 1 <= int(choice) <= len(self.items):
            clear_terminal()
            return self.items[int(choice) - 1].execute(game)
        elif choice == str(len(self.items) + 1):
            if self.parent:
                clear_terminal()
                return game.navigate_to(self.parent)
            elif self.name != "main_menu":
                clear_terminal()
                return game.navigate_to("main_menu")
            else:
                print("无效的选择，请重新输入。")
                return self.display(game)
        else:
            print("无效的选择，请重新输入。")
            return self.display(game)

from character.base_character import BaseCharacter
from card.base_card import BaseCard
from player.base_player import BasePlayer
from data.character import character_library_instance

class CharacterManager(Menu):
    def __init__(self, name, title, items, parent=None):
        self.name = name
        self.title = title
        self.items = items
        self.parent = parent
        self.characters = ["ch00001", "ch00001"]

    def display(self, game):
        self.display_character_info(self.characters[0])
        character_data = character_library_instance.character_data
        public_character = ["ch00001", "ch00002", "ch00003", "ch00004"]
        print(f"请选择玩家角色, 当前选择 '{character_data[self.characters[0]]['name']}':")
        print(f"[y] 确 认\t[n] 取 消")
        character_index = 0
        character_str = ""
        for character_id in public_character:
            character_index += 1
            character_str += f"[{character_index}] {character_data[character_id]['name']}\t"
        print(character_str)
        while True:
            try:
                user_input = input("请输入指令: ")

                if user_input.lower() == "y":
                    continue
                character_index = int(user_input) - 1
                self.characters[0] = public_character[character_index]
                clear_terminal()
                self.display(game)
            except ValueError:
                print(color_text(f"\t无效的索引, 请重新输入", "yellow"))
        return self.handle_choice(choice, game)
    
    def display_character_info(self, character_id):
        color_mapping = {
            "无": "gray",
            "风": "cyan",
            "火": "red",
            "山": "brown",
            "林": "green",
            "阴": "purple",
            "雷": "yellow",
        }
        # 根据 character_id 加载角色
        player = BasePlayer("player1", 1, character_id, "base", self)
        player.opponent = player
        print(player.character)
        same_card = []
        for card_id in player.character.cards:
            if card_id not in same_card:
                card = BaseCard.from_json(player, card_id)
                card_color = color_mapping[card.card_type.value]
                print(color_text(card, card_color))
            same_card.append(card_id)

menu_dict = {
    "main_menu": Menu("main_menu", "主菜单", [MenuItem("进入教程", "tutorial_menu"), MenuItem("对战AI", "pve_menu")]),
    "tutorial_menu": Menu(
        "tutorial_menu",
        "教程菜单",
        [
            MenuItem("时间与韧性, 打断与破绽", "time_and_resilience_tutorial"),
            MenuItem("先手与切换, 闪避与撤离", "dodge_and_retreat_tutorial"),
        ],
        parent="main_menu",
    ),
    "pve_menu": CharacterManager(
        "pve_menu",
        "选择玩家角色",
        [],
        parent="main_menu",
    ),
    "pve_enemy_menu": CharacterManager(
        "pve_enemy_menu",
        "选择对手角色",
        [MenuItem("剑士", "select_character", "ch00001", 1), MenuItem("近卫", "select_character", "ch00002", 1)],
        parent="pve_menu",
    ),
    "pve_start_menu": Menu(
        "pve_start_menu",
        "开始对战",
        [
            MenuItem("开始对战", "start_battle"),
        ],
    ),
}
