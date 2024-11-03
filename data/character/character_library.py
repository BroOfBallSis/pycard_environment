import os
import json


class CharacterLibrary:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CharacterLibrary, cls).__new__(cls)
        return cls._instance

    def __init__(self, character_directory=None):
        if not hasattr(self, "initialized"):  # 确保只初始化一次
            # 如果没有提供目录，则使用当前文件所在的目录
            if character_directory is None:
                character_directory = os.path.dirname(__file__)

            self.character_directory = character_directory
            self.character_data = self.load_character()
            self.initialized = True

    def load_character(self):
        """加载目录下的所有 JSON 文件，并将其合并为一个字典。"""
        character = {}
        for filename in os.listdir(self.character_directory):
            if filename.endswith(".json"):
                file_path = os.path.join(self.character_directory, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    character.update(data)  # 合并数据
        return character

    def get_character_info(self, character_id):
        """根据角色 ID 获取角色信息。"""
        return self.character_data.get(character_id)
