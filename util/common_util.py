import logging
import re
from urllib.parse import urlparse

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CommonUtil:
    def detail_handle(self,detail):
        if detail:
            index1 = detail.find("#")
            index2 = detail.find("*")

            if index1 != -1 and index2 != -1:
                index = min(index1, index2)
                substring = detail[index:]
                return re.sub(r'\*\*(.+?)\*\*', '### \\1', substring)
            elif index1 != -1:
                substring = detail[index1:]
                return re.sub(r'\*\*(.+?)\*\*', '### \\1', substring)
            elif index2 != -1:
                substring = detail[index2:]
                return re.sub(r'\*\*(.+?)\*\*', '### \\1', substring)
            else:
                return re.sub(r'\*\*(.+?)\*\*', '### \\1', detail)
        else:
            return None

    # 根据url提取域名/path，返回为-拼接的方式
    @staticmethod
    def get_name_by_url(url):
        if url:
            domain = urlparse(url).netloc
            path= urlparse(url).path
            if path and path.endswith("/"):
                path = path[:-1]
            return (domain.replace("www.","") + path.replace("/", "-")).replace(".", "-")
        else:
            return None

