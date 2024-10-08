import logging
import os
from typing import List, Optional
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Header, BackgroundTasks, HTTPException
from pydantic import BaseModel
from website_crawler import WebsitCrawler
import json
from insert_data_async import insert_website_data, update_website_detail, update_website_introduction, update_features

load_dotenv()

app = FastAPI()
website_crawler = WebsitCrawler()

system_auth_secret = os.getenv('AUTH_SECRET')\


# supabase数据库连接字符串
supabass_url = os.getenv('CONNECTION_SUPABASE_URL')

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 FileHandler 并将日志写入到文件中
log_file_path = './Log/main_api_log.txt'
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  # 确保目录存在
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

logger.info(f'Logging to file: {log_file_path}')
class URLRequest(BaseModel):
    url: str
    tags: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    category: str


class AsyncURLRequest(URLRequest):
    callback_url: str
    key: str


@app.post('/site/crawl')
async def scrape(request: URLRequest, authorization: Optional[str] = Header(None)):
    print(f'Received request: {request}')
    url = request.url
    tags = request.tags  # tag数组
    languages = request.languages  # 需要翻译的多语言列表
    category = request.category
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

    with open('./Log/res_data.json', 'a', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False)
        file.write('\n')

    print("INFO: Scraping data successfully. Waiting insert data to database.")
    logger.info("INFO: Scraping data successfully. Waiting insert data to database.")
    await insert_website_data(supabass_url, result, tags, category)
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

@app.post('/site/detail')
async def scrape_detail(request: URLRequest, authorization: Optional[str] = Header(None)):
    print(f'Received detail request: {request}')
    url = request.url
    tags = request.tags  # tag数组
    languages = request.languages  # 需要翻译的多语言列表
    category = request.category
    if system_auth_secret:
        # 配置了非空的auth_secret，才验证
        validate_authorization(authorization)

    result = await website_crawler.scrape_website_detail(url.strip(), languages)

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

    with open('./Data/Log.json', 'a', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False)
        file.write('\n')

    print("INFO: Scraping data successfully. Waiting insert data to database.")
    logger.info("INFO: Scraping data successfully. Waiting insert data to database.")
    await update_website_detail(supabass_url, result, tags, category)
    return response

@app.post('/site/introduction')
async def scrape_introduction(request: URLRequest, authorization: Optional[str] = Header(None)):
    print(f'Received detail request: {request}')
    url = request.url
    tags = request.tags
    languages = request.languages 
    category = request.category
    if system_auth_secret:
        # 配置了非空的auth_secret，才验证
        validate_authorization(authorization)

    result = await website_crawler.scrape_website_introduction(url.strip(), languages)

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

    with open('./Log/res_data.json', 'a', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False)
        file.write('\n')

    print("INFO: Scraping data successfully. Waiting insert data to database.")
    logger.info("INFO: Scraping data successfully. Waiting insert data to database.")
    await update_website_introduction(supabass_url, result, tags, category)
    return response

@app.post('/site/website_data')
async def scrape_website_data(request: URLRequest, authorization: Optional[str] = Header(None)):
    print(f'Received detail request: {request}')
    url = request.url
    tags = request.tags  # tag数组
    languages = request.languages  # 需要翻译的多语言列表
    category = request.category
    if system_auth_secret:
        # 配置了非空的auth_secret，才验证
        validate_authorization(authorization)

    result = await website_crawler.scrape_feature(url.strip(), languages)

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

    with open('./Log/res_data.json', 'a', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False)
        file.write('\n')

    print("INFO: Scraping data successfully. Waiting update_website_data  to database.")
    logger.info("INFO: Scraping data successfully. Waiting update_website_data  to database.")
    await update_features(supabass_url, result, tags, category)
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
