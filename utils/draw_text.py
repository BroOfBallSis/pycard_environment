import unicodedata
import os


def display_help():
    help_str = """
角色:
- 韧性: 通过造成韧性伤害来降低对手的韧性, 当韧性不大于0时, 获得 "打断" 状态
- 延迟: 双方手牌按照 "卡牌时间费用 + 延迟" 来决定结算的先后顺序, 结算的后手方, 按照结算时间的差值获得下一回合的 "延迟"
- 架势: 记录了角色上一回合出牌的 卡牌类型

卡牌:
- 基础: 基础卡牌 会在战斗开始时加入手牌, 且打出后不会进入弃牌堆
- 消耗: 消耗卡牌 在打出后离开手牌, 且不会进入弃牌堆, 而是从游戏中移除
- 先手: 玩家 "卡牌时间费用 + 延迟" 的值比对方小, 则满足条件, 执行下一个冒号';'前的效果
- 切换: 当前卡牌类型与角色架势不同, 且角色架势不为无, 则满足条件, 执行下一个冒号';'前的效果

状态:
- 闪避: 跳过所有 "对手 -> 自身" 的效果结算
- 打断: 跳过所有 "自身 -> 对手" 的效果结算, 回合结束时自身恢复全部韧性, 对手清空延迟
- 撤离: 跳过所有 "对手 -> 自身" 的效果结算, 回合结束时, 结束当前轮的战斗, 双方角色恢复韧性、体力、延迟, 并补充手牌至上限
- 破绽: 当自身延迟到达上限时, 清空延迟并获得破绽状态; 跳过出牌阶段, 直接打出1张 时间费用为6 的无效果 "破绽"

结算顺序:
- (立即) -> 先手方 -> 后手方 -> (收招)
- 即使是同时结算, 不同效果也有先后顺序, 一般的按照: 抵抗类 -> 状态类 -> 伤害类 -> 恢复类
    """
    print(help_str)


def clear_terminal(confirm=False):
    if confirm:
        input(color_text("输入回车键继续……", "gray"))
    # 检测操作系统并执行相应的清空命令
    if os.name == "nt":  # Windows
        os.system("cls")
    else:  # Unix/Linux/Mac
        os.system("clear")


def get_display_width(s):
    """计算字符串的显示宽度"""
    width = 0
    for char in s:
        if unicodedata.east_asian_width(char) in ("F", "W"):
            width += 2
        else:
            width += 1
    return width


def center_text(s, width):
    """将字符串居中对齐"""
    display_width = get_display_width(s)
    if display_width >= width:
        return s
    total_padding = width - display_width
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    return " " * left_padding + s + " " * right_padding


def color_text(text: str, color: str) -> str:
    """
    将输入文本转换为指定颜色的字符。

    :param text: 要转换的文本
    :param color: 颜色名称，可以是 'green', 'red', 'yellow', 'blue', 'purple', 'cyan', 'white'
    :return: 带有颜色的文本
    """
    color_codes = {
        "green": "\033[32m",
        "red": "\033[31m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m",
        "gray": "\033[90m",
        "brown": "\033[38;5;94m",  # 使用256色模式的棕色
    }

    if color not in color_codes:
        raise ValueError(f"Unsupported color: {color}")

    return f"{color_codes[color]}{text}{color_codes['reset']}"
