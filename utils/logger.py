import logging


class Logger:
    def __init__(self, player_name):
        self.player_name = player_name
        self.logger = logging.getLogger(player_name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(f"%(message)s")  # 只格式化消息部分
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message, level=0):
        # 根据 level 生成制表符前缀
        tab_prefix = "\t" * level
        # 组合制表符前缀、player_name 和消息
        formatted_message = f"{tab_prefix}{self.player_name}: {message}"
        # 记录信息
        self.logger.info(formatted_message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
