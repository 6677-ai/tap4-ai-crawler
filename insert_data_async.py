import json
import asyncio
import asyncpg
from datetime import datetime
from config import language_map
from config import fields
import os
from dotenv import load_dotenv

load_dotenv()

# 插入数据
async def insert_website_data(connection_string, json_data, tag, category):
    if json_data is None:
        print("ERROR: 获取数据失败，json_data 为 None")
        return
    if json_data.get("error"):
        print(f"INFO: 检测到错误信息 '{json_data.get('error')}'，停止插入数据。")
        return
    if json_data.get("title") in ["Just a moment...", "404"]:
        print(f"INFO: 检测到无效标题 '{json_data.get('title')}'，停止插入数据。")
        return
    if json_data.get("detail").startswith("### What is {product_name}?\n{product_name} is a"):
        print(f"INFO: 无效detail开头，停止插入数据。")
        return
    conn = None
    table_name = "web_navigation"

    category_name=category
    try:
        conn = await asyncpg.connect(dsn=connection_string, statement_cache_size=0)
        if conn:
            print("INFO: Connected to the database successfully.")
        async with conn.transaction():
            existing_data = await conn.fetchrow(
                'SELECT * FROM web_navigation WHERE category_name = $1 AND tag_name = $2 AND url = $3',
                json.dumps([category]), json.dumps(tag), json_data["url"]
            )
            data = {
                "name": json_data["name"],
                "collection_time": datetime.now(),
                "image_url": json_data["screenshot_data"],
                "url": json_data["url"],
                "thumbnail_url": json_data["screenshot_thumbnail_data"],
                "category_name": json.dumps([category_name]),
                "tag_name": json.dumps(tag),
            }
            for lang_data in json_data.get("languages", []):
                lang_code = lang_data["language"]
                lang_suffix = language_map.get(lang_code)
                if lang_suffix:
                    data[f"title_{lang_suffix}"] = lang_data.get("title")
                    data[f"content_{lang_suffix}"] = lang_data.get("description")
                    data[f"detail_{lang_suffix}"] = lang_data.get("detail")
                    data[f"introduction_{lang_suffix}"] = lang_data.get("introduction")
                    data[f"website_data_{lang_suffix}"] = lang_data.get("features")
            for field in fields:
                if field not in data:
                    data[field] = None
            if existing_data:
                update_id = existing_data['id']
                print('更新id为：', update_id)
                data.pop("id", None)
                update_set = ', '.join(f"{field} = ${i + 1}" for i, field in enumerate(data.keys()))
                # print('update_set',update_set)
                update_query = f'UPDATE {table_name} SET {update_set} WHERE id = ${len(data) + 1}'
                # print('update_sql',update_query)
                # if 'collection_time' in data:
                #     data['collection_time'] = data['collection_time'].isoformat() 
                # with open('data_output.json', 'w', encoding='utf-8') as f:
                #     json.dump(data, f, ensure_ascii=False, indent=4)  # 使用 json.dump 以美观的格式写入
                # print('data', data)
                await conn.execute(update_query, *data.values(), update_id)
                print("INFO: Data updated successfully.")
            else:
                max_id = await conn.fetchval('SELECT MAX(id) FROM web_navigation')
                new_id = (max_id + 1) if max_id is not None else 1
                data["id"] = new_id
                print('new_id', new_id)
                # print(tag)
                # 获取表结构中的所有列
                table_columns = await conn.fetch('SELECT column_name FROM information_schema.columns WHERE table_name = $1',
                                                table_name)
                table_columns = [col['column_name'] for col in table_columns]

                # 只插入表结构中存在的字段
                data_to_insert = {k: v for k, v in data.items() if k in table_columns}

                columns = ', '.join(data_to_insert.keys())
                values = ', '.join(f'${i + 1}' for i in range(len(data_to_insert)))
                query = f'INSERT INTO {table_name} ({columns}) VALUES ({values})'

                await conn.execute(query, *data_to_insert.values())
                print("INFO: Data inserted successfully.")
    except Exception as e:
        print("ERROR: Unable to connect to the database or execute query.")
        print(e)
    finally:
        if conn:
            await conn.close()
            print("INFO: Connection closed.")

async def check_existing_data(site_url, tags, category):
    connection_string = os.getenv('CONNECTION_SUPABASE_URL')
    print('site tags category:', site_url, tags, category)
    try:
        conn = await asyncpg.connect(connection_string)
        query = """
        SELECT id FROM web_navigation 
        WHERE url = $1 
        AND category_name @> $2::jsonb 
        AND tag_name @> $3::jsonb
        """
        result = await conn.fetchrow(query, site_url, json.dumps([category]), json.dumps(tags))
        await conn.close()
        return result is not None
    except Exception as e:
        print(f"INFO: Error checking existing data: {e}")
        return False

# 查找/更新网站的部分数据， field_name区分
async def update_website_field(connection_string, json_data, tag, category, field_name):
    # print('update_website_field:', field_name)
    if json_data is None or not json_data.get("url"):
        print(f"ERROR: 无效的 json_data 或缺少 URL")
        return
    conn = None
    table_name = "web_navigation"

    try:
        conn = await asyncpg.connect(dsn=connection_string, statement_cache_size=0)
        if conn:
            print("INFO: 成功连接到数据库。")
        
        async with conn.transaction():
            # 查找匹配的记录
            query = """
            SELECT id FROM web_navigation 
            WHERE url = $1 
            AND category_name @> $2::jsonb 
            AND tag_name @> $3::jsonb
            """
            row = await conn.fetchrow(query, json_data["url"], json.dumps([category]), json.dumps(tag))
            
            if row is None:
                print("INFO: 未找到匹配的记录，无法更新。")
                return

            record_id = row['id']
            
            # print(f"INFO: 正在更新id为{record_id}的{field_name}数据....")
            # 更新多语言字段
            for lang_data in json_data.get("languages", []):
                lang_code = lang_data["language"]
                lang_suffix = language_map.get(lang_code)
                if lang_suffix:
                    column_name = f"{field_name}_{lang_suffix}"
                    # print('更新数据的：column_name:', column_name)
                    update_query = f"""
                    UPDATE {table_name} 
                    SET {column_name} = $1 
                    WHERE id = $2
                    """
                    await conn.execute(update_query, lang_data[field_name], record_id)
                    print(f"INFO: 已更新 {column_name}")

            print(f"INFO: {field_name} 数据更新成功。")
    except Exception as e:
        print("ERROR: 无法连接到数据库或执行查询。")
        print(e)
    finally:
        if conn:
            await conn.close()
            print("INFO: 连接已关闭。")

async def update_website_detail(connection_string, json_data, tag, category):
    await update_website_field(connection_string, json_data, tag, category, "detail")

async def update_website_introduction(connection_string, json_data, tag, category):
    await update_website_field(connection_string, json_data, tag, category, "introduction")

async def update_features(connection_string, json_data, tag, category):
    await update_website_field(connection_string, json_data, tag, category, "website_data")

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


async def main():
    file_path = './Data/res_test.json'
    data = read_file(file_path)
    # AI工具,"[""AI常用工具""]"
    test_category = "AI工具"
    test_tag = ['AI常用工具']
    if data is not None:
        connection_string = os.getenv('CONNECTION_SUPABASE_URL')
        # await update_features(connection_string, data, test_tag, test_category)
        await insert_website_data(connection_string, data, test_tag, test_category)

if __name__ == "__main__":
    asyncio.run(main())
