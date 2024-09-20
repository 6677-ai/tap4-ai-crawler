import requests
import csv
from datetime import datetime


# 封装请求的函数
def send_proxy_request(site_url, tags, category, log_file_path):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 4487f197tap4ai8Zh42Ufi6mAHdfdf"
    }
    data = {
        "url": site_url,
        "tags": tags,
        "languages": ["zh-CN", "zh-TW", "en", "German", "es", "fr", "Japanese", "Portuguese", "ru"],
        "category": category
    }

    print(f'Post data: {data}')
    try:
        response = requests.post(
            url="http://127.0.0.1:8040/site/crawl",
            headers=headers,
            json=data,
            timeout=700
        )
        if response.status_code == 200:
            log_message = f"{datetime.now()} - INFO：{site_url} 请求成功\n"
            print(log_message.strip())
            with open(log_file_path, 'a') as log_file:
                log_file.write(log_message)
            return True
        else:
            log_message = f"{datetime.now()} - ERROR：{site_url} 状态码：{response.status_code}\n"
            print(log_message.strip())
            with open(log_file_path, 'a') as log_file:
                log_file.write(log_message)
            return False

    except requests.exceptions.RequestException as e:
        log_message = f"{datetime.now()} - ERROR：{site_url} 请求失败，错误信息: {e}\n"
        print(log_message.strip())
        with open(log_file_path, 'a') as log_file:
            log_file.write(log_message)
        return False


def load_site_data(file_path):
    """
    从 CSV 文件加载网站数据
    :param file_path: CSV 文件路径
    :return: 网站数据列表
    """
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        site_data = []
        for row in reader:
            site = row['site']
            categoty = row['category_name']
            tags = row['tags'].strip('][').split('", "')
            tags = [tag.strip().strip("'\"") for tag in tags]
            site_data.append((site, tags, categoty))

    return site_data


def handle_request(site_data, log_file_path):
    total_sites = len(site_data)
    
    # 打开CSV文件，准备逐行写入
    with open('./Data/website_data_flag.csv', 'w', newline='') as csvfile:
        fieldnames = ['site', 'tags', 'flag']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx, (site, tags, category) in enumerate(site_data):
            current_count = idx + 1
            log_message = f"{datetime.now()} - INFO：处理第 {current_count}/{total_sites} 条数据 - 站点 {site} 请求发送中...\n"
            
            print(log_message.strip())
            with open(log_file_path, 'a') as log_file:
                log_file.write(log_message)

            success = send_proxy_request(site, tags, category, log_file_path)
            if success:
                flag = 1
                log_message = f"{datetime.now()} - INFO：站点 {site} 请求返回True\n"
            else:
                flag = 0
                log_message = f"{datetime.now()} - ERROR：站点 {site} 请求返回参数错误\n"
            
            print(log_message.strip())
            with open(log_file_path, 'a') as log_file:
                log_file.write(log_message)

            writer.writerow({'site': site, 'tags': tags, 'flag': flag})
            csvfile.flush()  # 确保数据立即写入文件


# data_path = './Data/website_data.csv'
data_path = './Data/website_data_deduplicated.csv'
all_site_data = load_site_data(data_path)

# 打开日志文件，以追加模式写入
log_file_path = './Log/request_log.txt'
handle_request(all_site_data, log_file_path)

# 如上，在文件信息输出的时候，上面log写入好像是等全部的输出输出完成之后才写入文件，如果输出很多的话可能会造成缓存不足错误，请你改正并且把它变成有一条输出一条,同理，website_data_flag里面的数据也要有一条插入一条