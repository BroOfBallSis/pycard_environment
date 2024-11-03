import os
import json


class ItemLibrary:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ItemLibrary, cls).__new__(cls)
        return cls._instance

    def __init__(self, item_directory=None):
        if not hasattr(self, "initialized"):  # 确保只初始化一次
            # 如果没有提供目录，则使用当前文件所在的目录
            if item_directory is None:
                item_directory = os.path.dirname(__file__)

            self.item_directory = item_directory
            self.item_data = self.load_item()
            self.initialized = True

    def load_item(self):
        """加载目录下的所有 JSON 文件，并将其合并为一个字典。"""
        item = {}
        for filename in os.listdir(self.item_directory):
            if filename.endswith(".json"):
                file_path = os.path.join(self.item_directory, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    item.update(data)  # 合并数据
        return item

    def get_item_info(self, item_id):
        """根据角色 ID 获取角色信息。"""
        return self.item_data.get(item_id)
