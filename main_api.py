import logging
import os
from typing import List, Optional

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Header, BackgroundTasks, HTTPException
from pydantic import BaseModel

from website_crawler import WebsitCrawler

app = FastAPI()
website_crawler = WebsitCrawler()
load_dotenv()
system_auth_secret = os.getenv('AUTH_SECRET')

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class URLRequest(BaseModel):
    url: str
    tags: Optional[List[str]] = None
    languages: Optional[List[str]] = None


class AsyncURLRequest(URLRequest):
    callback_url: str
    key: str


@app.post('/site/crawl')
async def scrape(request: URLRequest, authorization: Optional[str] = Header(None)):
    url = request.url
    tags = request.tags  # tag数组
    languages = request.languages  # 需要翻译的多语言列表

    if system_auth_secret:
        # 配置了非空的auth_secret，才验证
        validate_authorization(authorization)

    result = await website_crawler.scrape_website(url.strip(), tags, languages)

    # 若result为None,则 code="10001"，msg="处理异常，请稍后重试"
    code = 200
    msg = 'success'
    if result is None:
        code = 10001
        msg = 'fail'

    # 将数据映射到 'data' 键下
    response = {
        'code': code,
        'msg': msg,
        'data': result
    }
    return response


@app.post('/site/crawl_async')
async def scrape_async(background_tasks: BackgroundTasks, request: AsyncURLRequest,
                       authorization: Optional[str] = Header(None)):
    url = request.url
    callback_url = request.callback_url
    key = request.key  # 请求回调接口，放header Authorization: 'Bear key'
    tags = request.tags  # tag数组
    languages = request.languages  # 需要翻译的多语言列表

    if system_auth_secret:
        # 配置了非空的auth_secret，才验证
        validate_authorization(authorization)

    # 直接发起异步请求:使用background_tasks后台运行
    background_tasks.add_task(async_worker, url.strip(), tags, languages, callback_url, key)

    # 若result为None,则 code="10001"，msg="处理异常，请稍后重试"
    code = 200
    msg = 'success'
    response = {
        'code': code,
        'msg': msg
    }
    return response


def validate_authorization(authorization):
    if not authorization:
        raise HTTPException(status_code=400, detail="Missing Authorization header")
    if 'Bearer ' + system_auth_secret != authorization:
        raise HTTPException(status_code=401, detail="Authorization is error")


async def async_worker(url, tags, languages, callback_url, key):
    # 爬虫处理封装为一个异步任务
    result = await website_crawler.scrape_website(url.strip(), tags, languages)
    # 通过requests post 请求调用call_back_url， 携带参数result， heaer 为key
    try:
        logger.info(f'callback begin:{callback_url}')
        response = requests.post(callback_url, json=result, headers={'Authorization': 'Bearer ' + key})
        if response.status_code != 200:
            logger.error(f'callback error:{callback_url}', response.text)
        else:
            logger.info(f'callback success:{callback_url}')
    except Exception as e:
        logger.error(f'call_back exception:{callback_url}', e)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8040)
