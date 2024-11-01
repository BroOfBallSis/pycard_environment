import unicodedata
import os


def clear_terminal():
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
