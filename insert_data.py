import psycopg2
from psycopg2 import sql
import json
from datetime import datetime
from config import language_map
from config import fields
from dotenv import load_dotenv
import os

load_dotenv()


def insert_website_data(connection_string, json_data):
    """
    Inserts website data into a PostgreSQL database.
    :param connection_string: Database connection string
    """
    if json_data is None:
        print("ERROR: 获取数据失败，json_data 为 None")
        return
    # 表名
    table_name = "web_navigation"
    # print('连接字符串', connection_string)
    # 初始化
    cur = None
    conn = None
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                print("INFO: Connected to the database successfully.")
                cur.execute(sql.SQL("SELECT MAX(id) FROM {}").format(sql.Identifier(table_name)))
                max_id = cur.fetchone()[0]
                new_id = (max_id + 1) if max_id is not None else 1
                # 构建数据
                data = {
                    "id": new_id,
                    "collection_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S%z"),
                    "name": json_data["name"],
                    "url": json_data["url"],
                    "thumbnail_url": json_data["screenshot_thumbnail_data"],
                    "image_url": json_data["screenshot_data"],
                    "description": json_data["description"],
                    "detail": json_data["detail"],
                    "screenshot_data": json_data["screenshot_data"],
                    "tag_name": json.dumps(json_data["tags"]),
                    "languages": json.dumps(json_data["languages"]),
                    "category_name": json_data.get("category_name", None),
                }
                # 添加多语言字段
                for lang_data in json_data.get("languages", []):
                    lang_code = lang_data["language"]
                    lang_suffix = language_map.get(lang_code)
                    if lang_suffix:
                        data[f"title_{lang_suffix}"] = lang_data.get("title")
                        data[f"content_{lang_suffix}"] = lang_data.get("description")
                        data[f"detail_{lang_suffix}"] = lang_data.get("detail")
                        data[f"introduction_{lang_suffix}"] = lang_data.get("introduction")
                        data[f"website_data_{lang_suffix}"] = lang_data.get("website_data")
                # 赋空值确保有数据
                for field in fields:
                    if field not in data:
                        data[field] = None

                # 插入SQL
                insert_query = sql.SQL(
                    "INSERT INTO {table} ({fields}) VALUES ({values})"
                ).format(
                    table=sql.Identifier(table_name),
                    fields=sql.SQL(', ').join(map(sql.Identifier, fields)),
                    values=sql.SQL(', ').join(sql.Placeholder() * len(fields))
                )
                cur.execute(insert_query, tuple(data[field] for field in fields))
                conn.commit()
                print("INFO: Data inserted successfully.")
                return
    except psycopg2.Error as e:
        print("ERROR: Unable to connect to the database or execute query.")
        print(e)


def read_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file}")
        return None

# if __name__ == "__main__":
#     file_path = './Data/res_data1.json'
#     data = read_file(file_path)
#     if data is not None:
#         supabase_url = os.getenv('CONNECTION_SUPABASE_URL')
#         insert_website_data(supabase_url, data)
