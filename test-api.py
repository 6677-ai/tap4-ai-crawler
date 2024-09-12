import json
import requests
import csv

#  "tags": [ "selected tags: ai-detector","chatbot","text-writing","image","code-it"]}
tags = ["selected tags: proxy"]


# languages = ["zh-CN", "zh-TW", "de", "en", "es", "fr", "jp", "pt", "ru"]
# ["zh-CN", "zh-TW", "German", "English", "Spanish", "French", "Japanese", "Portuguese", "Russian"]

# 封装请求的函数
def send_proxy_request(site_url, tags):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 4487f197tap4ai8Zh42Ufi6mAHdfdf"
    }
    data = {
        "url": site_url,
        "tags": tags,
        "languages": ["zh-CN", "zh-TW", "German", "en", "es", "fr", "Japanese", "Portuguese", "ru"],
    }

    json_data = json.dumps(data)

    response = requests.post(
        url="http://127.0.0.1:8040/site/crawl",
        headers=headers,
        data=json_data
    )

    return response


def test(site):
    print('Site data has been read:', site)


# for site_data in sites_data:
#     site_url = site_data["Site"]
#
#     # 发送请求
#     response = send_proxy_request(site_url, tags)

#  CSV 文件路径
csv_file_path = './Data/website_data.csv'


def read_site_file(file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            json_string = row[0]
            try:
                data = json.loads(json_string)
                site = data.get('Site')
                if site:
                    # send_proxy_request(site, tags)
                    test(site)
                else:
                    print("Site not found in JSON data.")

            except json.JSONDecodeError:
                print("Error decoding JSON from row:", json_string)


send_proxy_request("https://anyip.io/", tags)
