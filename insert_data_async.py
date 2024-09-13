import json
import asyncio
import asyncpg
from datetime import datetime
from config import language_map
from config import fields
# url = "postgresql://postgres.olagznauomwldwnluuek:hyz040506sadasdads@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?gssencmode=disable"


async def insert_website_data(connection_string, json_data):
    if json_data is None:
        print("ERROR: 获取数据失败，json_data 为 None")
        return
    conn = None
    table_name = "web_navigation"

    print('database_string', connection_string)
    try:
        conn = await asyncpg.connect(dsn=connection_string)
        if conn:
            print("INFO: Connected to the database successfully.")
        async with conn.transaction():
            max_id = await conn.fetchval('SELECT MAX(id) FROM web_navigation_demo')
            new_id = (max_id + 1) if max_id is not None else 1
            print('new_id', new_id)
            data = {
                "id": new_id,
                "name": json_data["name"],
                "collection_time": datetime.now(),
                "image_url": json_data["screenshot_data"],
                "url": json_data["url"],
                "thumbnail_url": json_data["screenshot_thumbnail_data"],
                "category_name": json_data.get("category_name", None),
                "tag_name": json.dumps(json_data["tags"]),

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
            for field in fields:
                if field not in data:
                    data[field] = None

            columns = ', '.join(data.keys())
            values = ', '.join(f'${i + 1}' for i in range(len(data)))
            query = f'INSERT INTO {table_name} ({columns}) VALUES ({values})'

            await conn.execute(query, *data.values())
            print("INFO: Data inserted successfully.")
    except Exception as e:
        print("ERROR: Unable to connect to the database or execute query.")
        print(e)
    finally:
        await conn.close()


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


# async def main():
#     file_path = './Data/response.json'
#     connection_string = "postgresql://postgres.olagznauomwldwnluuek:hyz040506sadasdads@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?gssencmode=disable"
#
#     data = read_file(file_path)
#     if data is not None:
#         await insert_website_data(connection_string, data)
#

# if __name__ == "__main__":
#     asyncio.run(main())


