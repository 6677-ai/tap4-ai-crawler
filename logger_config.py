import logging

def setup_logger():
    # ������־��¼��
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # �����ļ���������������־д���ļ�
    file_handler = logging.FileHandler("./Log/main_api_log.txt")
    file_handler.setLevel(logging.INFO)

    # ��������̨��������������־���������̨
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # ������־��ʽ����
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # ����������ӵ���־��¼��
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger