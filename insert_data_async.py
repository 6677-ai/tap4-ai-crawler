import json
import asyncio
import asyncpg
import csv
import os
from datetime import datetime
from config import language_map
from config import fields
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')

def validate_json_data(json_data):
    # print('json_data', json_data)
    if json_data is None:
        print("ERROR: 获取数据失败，json_data 为 None")
        return False
    if json_data.get("error"):
        print(f"INFO: 检测到错误信息 '{json_data.get('error')}'，停止插入数据。")
        return False
    if json_data.get("title") in ["Just a moment...", "404"]:
        print(f"INFO: 检测到无效标题 '{json_data.get('title')}'，停止插入数据。")
        return False
    if json_data.get("detail", "").startswith("### What is {product_name}?\n{product_name} is a"):
        print(f"INFO: 无效detail开头，停止插入数据。")
        return False
    return True

# 插入数据
async def insert_website_data(connection_string, json_data, tag, category):
    """更新/插入数据库数据"""
    if not validate_json_data(json_data):
        return
    conn = None
    schema_name = "ziniao"
    table_name = "web_navigation"
    category_name=category
    try:
        conn = await asyncpg.connect(dsn=connection_string,statement_cache_size=0)
        if conn:
            print("INFO: Connected to the database successfully.")
        async with conn.transaction():
            select_query = f'SELECT * FROM {schema_name}.{table_name} WHERE category_name = $1 AND tag_name = $2 AND url = $3'
            existing_data = await conn.fetchrow(
                select_query,
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
            # 处理多语言
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
                update_query = f'UPDATE {schema_name}.{table_name} SET {update_set} WHERE id = ${len(data) + 1}'
                await conn.execute(update_query, *data.values(), update_id)
                print("INFO: Data updated successfully.")
            else:
                select_id_query = f'SELECT MAX(id) FROM {schema_name}.{table_name}'
                max_id = await conn.fetchval(select_id_query)
                new_id = (max_id + 1) if max_id is not None else 1
                data["id"] = new_id
                print('new_id', new_id)

                table_columns = await conn.fetch('SELECT column_name FROM information_schema.columns WHERE table_name = $1 AND table_schema = $2', table_name, schema_name)
                
                table_columns = [col['column_name'] for col in table_columns]

                # 只插入表结构中存在的字段
                data_to_insert = {k: v for k, v in data.items() if k in table_columns}

                if not data_to_insert:
                    print("ERROR: No data to insert.")
                    return
                columns = ', '.join(data_to_insert.keys())
                values = ', '.join(f'${i + 1}' for i in range(len(data_to_insert)))
                query = f'INSERT INTO {table_name} ({columns}) VALUES ({values})'

                await conn.execute(query, *data_to_insert.values())
                print("INFO: Data inserted successfully.")
    except Exception as e:
        print("ERROR: Unable to connect to the database or execute query.")
        print(e)
        if hasattr(e, 'pgcode'):
            print(f"Postgres error code: {e.pgcode}")
        if hasattr(e, 'pgerror'):
            print(f"Postgres error message: {e.pgerror}")
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
        SELECT id FROM ziniao.web_navigation 
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

# 将csv文件里面的数据放入
async def insert_data_from_csv(connection_string, csv_file_path, table_name):
    conn = None
    try:
        conn = await asyncpg.connect(dsn=connection_string, statement_cache_size=0)
        print("INFO: Connected to the database successfully.")

        # 查询目标表的列类型信息
        query_column_types = f"""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = $1;
        """
        column_info = await conn.fetch(query_column_types, table_name)
        
        column_types = {col['column_name']: col['data_type'] for col in column_info}
        
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 构建插入查询
                columns = ', '.join(row.keys())
                values = ', '.join(f'${i + 1}' for i in range(len(row)))
                query = f'INSERT INTO {table_name} ({columns}) VALUES ({values})'
                
                # 将每个字段的数据转换为适合的类型
                formatted_values = []
                for col, value in row.items():
                    col_type = column_types.get(col)

                    if col_type == 'integer':
                        formatted_values.append(int(value))
                    elif col_type in ['double precision', 'numeric', 'real']:
                        formatted_values.append(float(value))
                    elif col_type == 'boolean':
                        formatted_values.append(value.lower() in ['true', 't', 'yes', '1'])
                    elif col_type == 'jsonb':
                        formatted_values.append(value) 
                    elif col_type == 'date':
                        formatted_values.append(datetime.strptime(value, '%Y-%m-%d').date())
                    elif col_type == 'timestamp' or col_type == 'timestamp with time zone':
                        try:
                            formatted_values.append(datetime.strptime(value, '%Y-%m-%d %H:%M:%S'))
                        except ValueError:
                            formatted_values.append(datetime.strptime(value, '%Y-%m-%dT%H:%M:%S'))
                    else:
                        formatted_values.append(value) 

                await conn.execute(query, *formatted_values)
                print(f"INFO: Inserted row: {row}")

    except Exception as e:
        print("ERROR: Unable to connect to the database or execute query.")
        print(e)
    finally:
        if conn:
            await conn.close()
            print("INFO: Connection closed.")


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
    # connection_string = os.getenv('CONNECTION_SUPABASE_URL')
    # csv导入数据
    # csv_file_path = './util/file_util/Data/tes.csv' 
    # csv_file_path = './util/file_util/Data/saved_file.csv' 
    table_name = 'ziniao.web_navigation'
    # await insert_data_from_csv(connection_string, csv_file_path, table_name)

    file_path = './Data/res_test.json'
    data = read_file(file_path)
    test_category = "AI工具"
    test_tag = ['AI常用工具']
    if data is not None:
        connection_string = os.getenv('CONNECTION_SUPABASE_URL')
        # print('connection_string',connection_string)
        # await update_features(connection_string, data, test_tag, test_category)
        await insert_website_data(connection_string, data, test_tag, test_category)

if __name__ == "__main__":
    asyncio.run(main())
