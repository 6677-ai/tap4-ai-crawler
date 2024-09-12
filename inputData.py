import psycopg2
from psycopg2 import sql
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


# 数据库字段
# fields = [
#     "id",
#     "name",
#     "tag_name",
#     "category_name",
#     "url",
#     "thumbnail_url",
#     "image_url",
#     "collection_time",
#     "star_rating",
#     "title_en",
#     "content_en",
#     "detail_en",
#     "introduction_en",
#     "website_data_en",
#     "title_cn",
#     "content_cn",
#     "introduction_cn",
#     "website_data_cn",
#     "detail_cn",
#     "website_data_de",
#     "website_data_es",
#     "website_data_fr",
#     "website_data_jp",
#     "website_pt",
#     "website_data_ru",
#     "website_data_tw",
#     "detail_de",
#     "detail_es",
#     "detail_fr",
#     "detail_jp",
#     "detail_pt",
#     "detail_ru",
#     "detail_tw",
#     "introduction_de",
#     "introduction_es",
#     "introduction_fr",
#     "introduction_jp",
#     "introduction_pt",
#     "introduction_tw",
#     "introduction_ru",
#     "title_de",
#     "title_es",
#     "title_fr",
#     "title_jp",
#     "title_pt",
#     "title_ru",
#     "title_tw",
#     "content_de",
#     "content_es",
#     "content_fr",
#     "content_pt",
#     "content_jp",
#     "content_ru",
#     "content_tw"
# ]

def insert_website_data(connection_string, json_data):
    """
    Inserts website data into a PostgreSQL database.
    :param connection_string: Database connection string
    """
    # 表名
    table_name = "websiteData-demo"
    try:
        conn = psycopg2.connect(connection_string)
        print("INFO: Connected to the database successfully.")
        cur = conn.cursor()

        cur.execute(sql.SQL("SELECT MAX(id) FROM {}").format(sql.Identifier(table_name)))
        max_id = cur.fetchone()[0]
        new_id = (max_id + 1) if max_id is not None else 1
        print("json_data['name']", json_data["name"])
        fields = [
            "id",
            "created_dt",
            "name",
            "url",
            "title",
            "description",
            "detail",
            "screenshot_data",
            "tags",
            "languages"
        ]

        data = (
            new_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            json_data["name"],
            json_data["url"],
            json_data["title"],
            json_data["description"],
            json_data["detail"],
            json_data["screenshot_data"],
            json.dumps(json_data["tags"]),
            json.dumps(json_data["languages"]),
        )
        #sql语句
        insert_query = sql.SQL(
            "INSERT INTO {table} ({fields}) VALUES ({values})"
        ).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, fields)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(fields))
        )
        # # for language_info in json_data["languages"]:
        # #     language = language_info.get("language")
        # #     title = language_info.get("title")
        # #     description = language_info.get("description")
        # #     detail = language_info.get("detail")

        # 执行sql
        cur.execute(insert_query, data)
        conn.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Unable to connect to the database or execute query.")
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


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


if __name__ == "__main__":
    file_path = './Data/res_data.json'
    data = read_file(file_path)
    if data is not None:
        supabase_url = os.getenv('CONNECTION_SUPABASE_URL')
        insert_website_data(supabase_url, data)
