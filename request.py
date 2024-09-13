import requests
import json
import csv
import time


# 封装请求的函数
def send_proxy_request(site_url, tags):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 4487f197tap4ai8Zh42Ufi6mAHdfdf"
    }
    data = {
        "url": site_url,
        "tags": tags,
        "languages": ["zh-CN", "zh-TW", "en", "German", "es", "fr", "Japanese", "Portuguese", "ru"],
    }

    try:
        response = requests.post(
            url="http://127.0.0.1:8040/site/crawl",
            headers=headers,
            json=data,
            timeout=300
        )
        print(response.json())
        if response.status_code == 200:
            print(f"INFO：{site_url} 请求成功")
            return True
        else:
            print(f"ERROR：{site_url} 状态码：{response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"ERROR：{site_url} 请求失败，错误信息: {e}")
        return False


def load_site_data(file_path):
    """
    从 CSV 文件加载网站数据
    :param file_path: CSV 文件路径
    :return: 网站数据列表
    """
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        site_data = []
        for row in reader:
            site = row['site']
            tags = row['tags'].strip('][').split('", "')
            site_data.append((site, tags))
    return site_data


def interactive_request_process(site_data):
    """
    交互式处理网站请求
    :param site_data: 包含网站和标签数据的列表
    :return: None
    """
    for idx, (site, tags) in enumerate(site_data):
        input(f"按回车键来处理下一个站点 [{idx + 1}/{len(site_data)}]：{site}")
        # success = test(site, tags)
        print(f"INFO：站点 {site} 请求发送中...")
        success = send_proxy_request(site, tags)
        if success:
            print(f"INFO：站点 {site} 请求返回True")
            flag = 1
        else:
            flag = 0
            print(f"ERROR：站点 {site} 请求返回参数错误")
        site_data[idx] = (site, tags, flag)
    with open('./Data/website_data_flag.csv', 'w', newline='') as csvfile:
        fieldnames = ['site', 'tags', 'flag']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in site_data:
            writer.writerow({'site': item[0], 'tags': item[1], 'flag': item[2]})


file_path = './Data/website_data.csv'
site_data = load_site_data(file_path)

interactive_request_process(site_data)
