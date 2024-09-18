import logging

def setup_logger():
    # 创建日志记录器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # 创建文件处理器，并将日志写入文件
    file_handler = logging.FileHandler("./Log/main_api_log.txt")
    file_handler.setLevel(logging.INFO)

    # 创建控制台处理器，并将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建日志格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger