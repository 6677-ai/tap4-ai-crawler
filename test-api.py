import json
import requests
import csv

#  CSV 文件路径
csv_file_path = './Data/websiteDataAndTags.csv'

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
#     # 发送请求
#     response = send_proxy_request(site_url, tags)


def read_site_data_file(file_path):
    with open(file_path, 'r', encoding='utf-8',  errors='replace') as file:
        csv_reader = csv.DictReader(file)
        # print("Column names:", csv_reader.fieldnames)  # 打印列名
        for row in csv_reader:
            # 合并 page_type, page_location 和 page_usage
            page_type = json.loads(row.get('page_type', '[]'))
            page_location = json.loads(row.get('page_location', '[]'))
            page_usage = json.loads(row.get('page_usage', '[]'))

            # 合并并去重
            combined_array = list(set(page_type + page_location + page_usage))
            try:
                details = json.loads(row['details'])
                site = details.get('Site')
                if site:
                    print(f"Site: {site}, Combined Array: {combined_array}")
                    # send_proxy_request(site, combined_array)  # 这里是你实际调用的函数
                    # test(site)
                else:
                    print("Site not found in details.")
            except json.JSONDecodeError:
                print("Error decoding JSON from details:", row['details'])


# send_proxy_request("https://anyip.io/", tags)
if __name__ == '__main__':
    read_site_data_file(csv_file_path)
