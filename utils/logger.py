import logging

class Logger:
    _loggers = {}

    def __new__(cls, player_name):
        if player_name in cls._loggers:
            return cls._loggers[player_name]
        else:
            instance = super(Logger, cls).__new__(cls)
            cls._loggers[player_name] = instance
            return instance

    def __init__(self, player_name):
        if hasattr(self, 'initialized'):
            return
        self.player_name = player_name
        self.logger = logging.getLogger(player_name)
        
        # 移除已经存在的处理程序
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(f"%(message)s")  # 只格式化消息部分
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        self.initialized = True

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

# 示例用法
if __name__ == "__main__":
    logger1 = Logger("Player1")
    logger1.info("This is an info message from Player1")

    logger2 = Logger("Player2")
    logger2.info("This is an info message from Player2")

    logger3 = Logger("Player1")
    logger3.info("This is another info message from Player1")