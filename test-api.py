import json
import requests

aiUrl = "https://anyip.io/"
# 设置请求头部
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 4487f197tap4ai8Zh42Ufi6mAHdfdf"
}

# 设置请求体
data = {
    "url": aiUrl,
    "tags": ["selected tags: proxy"]
}

json_data = json.dumps(data)

response = requests.post(
    url="http://127.0.0.1:8040/site/crawl",
    headers=headers,
    data=json_data
)
