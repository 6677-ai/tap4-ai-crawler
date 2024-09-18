import requests
from bs4 import BeautifulSoup
import json


# base_url = "https://007tg.com"
# # 模拟用户
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }
#
# def fetch_html(url):
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.text
#     else:
#         print(f"请求失败，状态码: {response.status_code}")
#         return None

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    all_headers = soup.find_all('h4', class_='text-gray text-lg')
    output_data = {}
    for header in all_headers:
        if 'AI工具' in header.get_text(strip=True):
            specific_header = header
            break
    if specific_header:
        tab_name = specific_header.text.strip()
        print(f"一级标签: {tab_name}")
        output_data['一级标签'] = tab_name
        output_data['二级标签'] = {}
        # 查找后续二级标签的内容
        next_div = specific_header.find_next_sibling('div', class_='d-flex flex-fill flex-tab')
        if next_div:
            links = next_div.find_all('a', class_='nav-link')
            for link in links:
                tab_link = link['data-link']
                tab_href = link['href']
                link_text = link.text.strip()
                print(f" 二级标签：{link_text}: {tab_link}: {tab_href}")
                tab_id = link['href'].replace('#', '')

                # 模拟点击二级标签，获取其内容
                tab_content_div = soup.find('div', id=tab_id)
                if tab_content_div:
                    url_cards = tab_content_div.find_all('div', class_='url-body')
                    sub_tab_data = []
                    for url_card in url_cards:
                        a_tag = url_card.find('a')
                        if a_tag and 'data-url' in a_tag.attrs:
                            data_url = a_tag['data-url']
                            title = a_tag.find('strong').get_text(strip=True)
                            print(f"    name: {title}, url: {data_url}")
                            sub_tab_data.append({
                                'url': data_url,
                                'name': title
                            })
                    output_data['二级标签'][link_text] = sub_tab_data
                else:
                    print(f"  没有找到 {link_text} 的工具内容")
    return output_data


# 获取主页内容
# main_html = fetch_html(base_url)
# if main_html:
with open('response.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
    output_data = parse_html(html_content)

    # 将数据保存为 JSON 文件
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)
    print("数据已保存到 data.json")
