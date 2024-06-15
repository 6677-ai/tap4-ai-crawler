import asyncio
import logging
from flask import Flask, request, jsonify
from website_crawler import WebsitCrawler

app = Flask(__name__)
website_crawler = WebsitCrawler()

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/site/crawl', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    tags = data.get('tags')  # tag数组
    languages = data.get('languages')  # 需要翻译的多语言列表

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(website_crawler.scrape_website(url.strip(), tags, languages))

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
    return jsonify(response)


if __name__ == '__main__':
    asyncio.run(app.run(host='0.0.0.0', port=8040, threaded=False))
