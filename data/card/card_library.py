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


if __name__ == "__main__":
    # 创建 CardLibrary 实例
    card_library = CardLibrary()

    # 获取所有卡牌信息
    all_cards = card_library.card_data

    # 将卡牌信息转换为列表并按 card_id 排序
    sorted_cards = sorted(all_cards.items(), key=lambda item: item[0])  # item[0] 是 card_id

    # 将排序后的卡牌信息转换为字典
    sorted_card_dict = {card_id: card_info for card_id, card_info in sorted_cards}

    # 写入新的 JSON 文件
    output_file_path = os.path.join(card_library.card_directory, "all/sorted_cards.json")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(sorted_card_dict, output_file, ensure_ascii=False, indent=4)

    print(f"Sorted card data has been written to {output_file_path}")
