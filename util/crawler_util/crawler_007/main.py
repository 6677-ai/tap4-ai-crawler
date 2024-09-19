# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://007tg.com/',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}


def fetch_content(url, params=None):
    try:
        print(f"正在请求: {url}")
        print(f"参数: {params}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        print(f"请求成功，状态码: {response.status_code}")
        return response.text
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def parse_html(html_content):
    print("开始解析HTML内容")
    soup = BeautifulSoup(html_content, 'html.parser')
    all_headers = soup.find_all('h4', class_='text-gray text-lg')
    data = []

    for header in all_headers:
        first_level_label = header.text.strip()
        print(f"一级标签: {first_level_label}")

        first_level_data = {
            'name': first_level_label,
            'children': []
        }

        next_div = header.find_next_sibling('div', class_='d-flex flex-fill flex-tab')
        if next_div:
            links = next_div.find_all('a', class_='nav-link')
            for link in links:
                second_level_label = link.text.strip()
                second_level_href = link['href']
                print(f"  二级标签: {second_level_label}, href: {second_level_href}")

                second_level_data = {
                    'name': second_level_label,
                    'href': second_level_href,
                    'children': []
                }

                # 模拟AJAX请求获取tab内容
                tab_id = second_level_href.lstrip('#').split('-')[-1]
                ajax_url = "https://007tg.com/wp-admin/admin-ajax.php"
                params = {
                    'action': 'load_home_tab',
                    'taxonomy': 'favorites',
                    'id': tab_id,
                    'post_id': '0'
                }
                print(f"      正在获取tab内容，ID: {tab_id}")
                tab_content = fetch_content(ajax_url, params)
                time.sleep(1)  # 添加延迟以避免请求过于频繁

                if tab_content:
                    tab_soup = BeautifulSoup(tab_content, 'html.parser')
                    url_cards = tab_soup.find_all('div', class_='url-card')
                    print(f"      找到 {len(url_cards)} 个三级标签")
                    for card_index, card in enumerate(url_cards, 1):
                        a_tag = card.find('a')
                        if a_tag:
                            href = a_tag.get('data-url', '')
                            strong_tag = a_tag.find('strong')
                            if strong_tag:
                                name = strong_tag.text.strip()
                                print(f"        三级标签 {card_index}: {name}")
                                second_level_data['children'].append({
                                    'name': name,
                                    'url': href
                                })

                first_level_data['children'].append(second_level_data)

        data.append(first_level_data)

    print("HTML解析完成")
    return data


if __name__ == "__main__":
    url = "https://007tg.com/"
    print(f"开始获取网页内容: {url}")
    html_content = fetch_content(url)

    if html_content:
        print("网页内容获取成功，开始解析")
        output_data = parse_html(html_content)

        if output_data:
            print("正在将数据保存到 data_007.json")
            with open('data_007.json', 'w', encoding='utf-8') as json_file:
                json.dump(output_data, json_file, ensure_ascii=False, indent=4)
            print("数据已成功保存到 data_007.json")
        else:
            print("解析 HTML 失败，未生成数据")
    else:
        print("获取网页内容失败")

    print("程序执行完毕")