import psycopg2
from psycopg2 import sql
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

supabass_url = os.getenv('CONNECTION_SUPABASS_URL')
def insert_website_data(connection_string, json_data):
    """
    Inserts website data into a PostgreSQL database.
    :param connection_string: Database connection string
    """
    table_name = "websiteData-demo"
    try:
        conn = psycopg2.connect(connection_string)
        print(conn)
        print("Connected to the database successfully.")
        cur = conn.cursor()

        # Query the maximum id in the table
        cur.execute(sql.SQL("SELECT MAX(id) FROM {}").format(sql.Identifier(table_name)))
        max_id = cur.fetchone()[0]
        new_id = (max_id + 1) if max_id is not None else 1
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
        insert_query = sql.SQL(
            "INSERT INTO {} (id, creat_dt, name, url, title, description, detail, screenshot_data, tags, languages) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        ).format(
            sql.Identifier(table_name)
        )
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


# insert_website_data(string, json_data)
