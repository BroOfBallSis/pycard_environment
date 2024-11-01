import os
import json


class CharacterLibrary:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CharacterLibrary, cls).__new__(cls)
        return cls._instance

    def __init__(self, characters_directory=None):
        if not hasattr(self, "initialized"):  # 确保只初始化一次
            # 如果没有提供目录，则使用当前文件所在的目录
            if characters_directory is None:
                characters_directory = os.path.dirname(__file__)

            self.characters_directory = characters_directory
            self.characters_data = self.load_characters()
            self.initialized = True

    def load_characters(self):
        """加载目录下的所有 JSON 文件，并将其合并为一个字典。"""
        characters = {}
        for filename in os.listdir(self.characters_directory):
            if filename.endswith(".json"):
                file_path = os.path.join(self.characters_directory, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    characters.update(data)  # 合并数据
        return characters

    def get_character_info(self, character_id):
        """根据角色 ID 获取角色信息。"""
        return self.characters_data.get(character_id)
