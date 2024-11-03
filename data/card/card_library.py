import os
import json


class CardLibrary:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CardLibrary, cls).__new__(cls)
        return cls._instance

    def __init__(self, card_directory=None):
        if not hasattr(self, "initialized"):  # 确保只初始化一次
            # 如果没有提供目录，则使用当前文件所在的目录
            if card_directory is None:
                card_directory = os.path.dirname(__file__)

            self.card_directory = card_directory
            self.card_data = self.load_card()
            self.initialized = True

    def load_card(self):
        """加载目录下的所有 JSON 文件，并将其合并为一个字典。"""
        card = {}
        for filename in os.listdir(self.card_directory):
            if filename.endswith(".json"):
                file_path = os.path.join(self.card_directory, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    card.update(data)  # 合并数据
        return card

    def get_card_info(self, card_id):
        """根据卡牌 ID 获取卡牌信息。"""
        return self.card_data.get(card_id)
