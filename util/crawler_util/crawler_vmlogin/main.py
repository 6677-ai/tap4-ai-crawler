# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.vmlogin.cc/dh/',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
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
    sidebar_menu = soup.find('div', class_='sidebar-menu-inner')
    if not sidebar_menu:
        print("未找到 sidebar-menu-inner 类")
        return None

    data = []
    first_level_items = sidebar_menu.find_all('li', class_='sidebar-item')
    print(f"找到 {len(first_level_items)} 个一级标签")

    for index, li in enumerate(first_level_items, 1):
        print(f"正在处理第 {index} 个一级标签")
        first_level_a = li.find('a', class_='smooth')
        if not first_level_a:
            print("  跳过：未找到一级标签的链接")
            continue

        first_level_label = first_level_a.find('span').text.strip()
        print(f"  一级标签名称: {first_level_label}")

        first_level_data = {
            'name': first_level_label,
            'children': []
        }

        sub_ul = li.find('ul')
        if sub_ul:
            second_level_items = sub_ul.find_all('li')
            print(f"  找到 {len(second_level_items)} 个二级标签")
            for sub_index, sub_li in enumerate(second_level_items, 1):
                print(f"    正在处理第 {sub_index} 个二级标签")
                sub_a = sub_li.find('a', class_='smooth')
                if sub_a:
                    second_level_label = sub_a.find('span').text.strip()
                    second_level_href = sub_a.get('href', '').strip()
                    print(f"      二级标签名称: {second_level_label}")
                    print(f"      二级标签链接: {second_level_href}")

                    second_level_data = {
                        'name': second_level_label,
                        'href': second_level_href,
                        'children': []
                    }

                    # 模拟AJAX请求获取tab内容
                    tab_id = second_level_href.lstrip('#').split('-')[-1]
                    ajax_url = "https://www.vmlogin.cc/dh/wp-admin/admin-ajax.php"
                    params = {
                        'action': 'load_home_tab',
                        'taxonomy': 'favorites',
                        'id': tab_id,
                        'post_id': '0',
                        'sidebar': '0'
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
    print("开始从网络获取HTML内容")
    url = "https://www.vmlogin.cc/dh/"  # 替换为实际的URL
    html_content = fetch_content(url)
    
    if html_content:
        print("HTML内容获取成功")
        print("开始解析HTML内容")
        output_data = parse_html(html_content)

        if output_data:
            print("正在将数据保存到 data.json")
            with open('data.json', 'w', encoding='utf-8') as json_file:
                json.dump(output_data, json_file, ensure_ascii=False, indent=4)
            print("数据已成功保存到 data.json")
        else:
            print("解析 HTML 失败，未生成数据")
    else:
        print("获取 HTML 内容失败")

    print("程序执行完毕")