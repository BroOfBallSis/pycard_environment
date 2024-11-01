import os
import json


class CardLibrary:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CardLibrary, cls).__new__(cls)
        return cls._instance

    def __init__(self, cards_directory=None):
        if not hasattr(self, "initialized"):  # 确保只初始化一次
            # 如果没有提供目录，则使用当前文件所在的目录
            if cards_directory is None:
                cards_directory = os.path.dirname(__file__)

            self.cards_directory = cards_directory
            self.cards_data = self.load_cards()
            self.initialized = True

    def load_cards(self):
        """加载目录下的所有 JSON 文件，并将其合并为一个字典。"""
        cards = {}
        for filename in os.listdir(self.cards_directory):
            if filename.endswith(".json"):
                file_path = os.path.join(self.cards_directory, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    cards.update(data)  # 合并数据
        return cards

    def get_card_info(self, card_id):
        """根据卡牌 ID 获取卡牌信息。"""
        return self.cards_data.get(card_id)
