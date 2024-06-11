import os
import time
from dotenv import load_dotenv
import logging
from io import BytesIO
import requests
from botocore.client import Config
import boto3
from datetime import datetime
import random
from PIL import Image
from urllib.parse import urlparse

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OSSUtil:
    def __init__(self):
        load_dotenv()
        self.S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
        self.S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID')
        self.S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
        self.S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
        self.S3_CUSTOM_DOMAIN = os.getenv('S3_CUSTOM_DOMAIN')
        self.s3 = boto3.client(
            's3',
            endpoint_url=self.S3_ENDPOINT_URL,
            aws_access_key_id=self.S3_ACCESS_KEY_ID,
            aws_secret_access_key=self.S3_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4')  # 使用S3兼容签名版本
        )

    def get_default_file_key(self, url, is_thumbnail=False):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        # 根据url生成名字
        image_name = None
        if url:
            domain = urlparse(url).netloc
            path= urlparse(url).path
            if path and path.endswith("/"):
                path = path[:-1]
            image_name = (domain.replace("www.","") + path.replace("/", "-")).replace(".", "-")
        else:
            image_name = random.randint(1, 1000)  # 生成随机值，范围可根据需求调整
        # 如果is_thumbnail True，则添加"thumbnail-"前缀
        if is_thumbnail:
            image_name = f"{image_name}-thumbnail"

        # 生成时间戳
        timestamp = int(time.time())
        # 构建默认的 file_key
        return f"tools/{year}/{month}/{day}/{image_name}-{timestamp}.png"

    def upload_file_to_r2(self, file_path, file_key):
        try:
            # 上传文件
            if file_path and 'http' in file_path:
                # 如果文件路径是URL
                response = requests.get(file_path, headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                })
                image_data = response.content
                self.s3.upload_fileobj(BytesIO(image_data), self.S3_BUCKET_NAME, file_key)
            else:
                self.s3.upload_file(file_path, self.S3_BUCKET_NAME, file_key)

            logger.info(f"文件 '{file_path}' 成功上传到 '{self.S3_BUCKET_NAME}/{file_key}'")
            if os.path.exists(file_path):
                os.remove(file_path)

            # 如果提供了自定义域名
            if self.S3_CUSTOM_DOMAIN:
                file_url = f"https://{self.S3_CUSTOM_DOMAIN}/{file_key}"
            else:
                file_url = f"{self.S3_ENDPOINT_URL}/{self.S3_BUCKET_NAME}/{file_key}"

            logger.info(f"文件URL: {file_url}")
            return file_url
        except Exception as e:
            logger.info(f"上传文件过程中发生错误: {e}")
            return None

    def generate_thumbnail_image(self, url, image_key):
        # 下载图像文件
        response = self.s3.get_object(Bucket=self.S3_BUCKET_NAME, Key=image_key)
        image_data = response['Body'].read()

        # 使用Pillow库打开图像
        image = Image.open(BytesIO(image_data))

        # 将图像缩放为50%
        width, height = image.size
        new_width = int(width * 0.5)
        new_height = int(height * 0.5)
        resized_image = image.resize((new_width, new_height))

        # 创建一个BytesIO对象来保存缩略图
        thumbnail_buffer = BytesIO()
        resized_image.save(thumbnail_buffer, format='PNG')
        thumbnail_buffer.seek(0)

        # 将缩略图上传回S3
        thumbnail_key = self.get_default_file_key(url, is_thumbnail=True)
        self.s3.put_object(Bucket=self.S3_BUCKET_NAME, Key=thumbnail_key, Body=thumbnail_buffer)

        # 如果提供了自定义域名
        if self.S3_CUSTOM_DOMAIN:
            file_url = f"https://{self.S3_CUSTOM_DOMAIN}/{thumbnail_key}"
        else:
            file_url = f"{self.S3_ENDPOINT_URL}/{self.S3_BUCKET_NAME}/{thumbnail_key}"
        logger.info(f"缩略图文件URL: {file_url}")
        return file_url
