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
    "pve_menu": Menu(
        "pve_menu",
        "选择玩家角色",
        [
            MenuItem("剑士", "select_character", "ch00001", 0),
            MenuItem("近卫", "select_character", "ch00002", 0),
            MenuItem("牧师", "select_character", "ch00003", 0),
        ],
        parent="main_menu",
    ),
    "pve_enemy_menu": Menu(
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
