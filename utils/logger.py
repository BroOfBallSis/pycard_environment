import logging
import os
import re
import sys
from datetime import datetime

class Logger:
    _loggers = {}
    _depth = 0

    def __new__(cls, name):
        if name in cls._loggers:
            return cls._loggers[name]
        else:
            instance = super(Logger, cls).__new__(cls)
            cls._loggers[name] = instance
            return instance

    def __init__(self, name):
        if hasattr(self, "initialized"):
            return
        self.name = name
        self.source_name = None
        self.logger = logging.getLogger(name)

        # 创建终端输出的 logger
        self.console_logger = logging.getLogger(f"{name}_console")
        if self.console_logger.hasHandlers():
            self.console_logger.handlers.clear()
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(f"%(message)s")  # 只格式化消息部分
        console_handler.setFormatter(console_formatter)
        self.console_logger.addHandler(console_handler)
        self.console_logger.setLevel(logging.INFO)

        # 创建文件输出的 logger
        self.file_logger = logging.getLogger(f"{name}_file")
        if self.file_logger.hasHandlers():
            self.file_logger.handlers.clear()
        log_dir = "log"
        os.makedirs(log_dir, exist_ok=True)
        log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_battle.log")
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(file_formatter)
        self.file_logger.addHandler(file_handler)
        self.file_logger.setLevel(logging.INFO)

        self.initialized = True
        self.__class__._depth = 0

    def set_source_name(self, source_name):
        self.source_name = source_name

    def set_depth(self, depth):
        self.__class__._depth = depth

    def increase_depth(self):
        # self.console_logger.info("increase_depth")
        self.__class__._depth += 1

    def decrease_depth(self):
        # self.console_logger.info("decrease_depth")
        if self.__class__._depth > 0:
            self.__class__._depth -= 1

    def info(self, message, show_source=True):
        # 根据 level 生成制表符前缀
        tab_prefix = "\t" * self.__class__._depth
        # 组合制表符前缀、player_name 和消息
        if show_source and self.source_name:
            formatted_message = f"{tab_prefix}{self.source_name}: {message}"
        else:
            formatted_message = f"{tab_prefix}{message}"
        # 记录信息
        self.console_logger.info(formatted_message)

    def log_to_file(self, message):
        # 根据 level 生成制表符前缀
        tab_prefix = "\t" * self.__class__._depth
        # 组合制表符前缀、player_name 和消息
        formatted_message = f"{tab_prefix}{message}"
        # 记录信息
        # self.console_logger.info(formatted_message)
        self.file_logger.warning(formatted_message)

    def debug(self, message):
        self.console_logger.debug(message)
        self.file_logger.debug(message)

    def warning(self, message):
        self.console_logger.warning(message)
        self.file_logger.warning(message)

    def error(self, message):
        self.console_logger.error(message)
        self.file_logger.error(message)

    def critical(self, message):
        self.console_logger.critical(message)
        self.file_logger.critical(message)
