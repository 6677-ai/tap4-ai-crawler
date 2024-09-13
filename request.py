import requests
import json

tags = ["selected tags: proxy"]


# 封装请求的函数
def send_proxy_request(site_url, tags) :
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 4487f197tap4ai8Zh42Ufi6mAHdfdf"
    }
    data = {
        "url": site_url,
        "tags": tags,
        "languages": ["zh-CN", "zh-TW", "en", "German", "es", "fr", "Japanese", "Portuguese", "ru"],
    }

    json_data = json.dumps(data)

    response = requests.post(
        url="http://127.0.0.1:8040/site/crawl",
        headers=headers,
        data=json_data
    )

    return response


send_proxy_request("anyip.io", tags)
# https://soax.com

# send_proxy_request("proxyma.io", tags)
# send_proxy_request("soax.com", tags)
# send_proxy_request("https://tattooease.net", tags)
