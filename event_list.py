import requests
from bs4 import BeautifulSoup
import json

import psycopg2

url = "https://www.chf.or.kr/cont/{}/all/month/menu/363?thisPage=1&idx={}&searchCategory1=&searchCategory2={}&searchField=all&searchDate={}&weekSel=&searchText="

# view or calendar (개별 이벤트, 전체이벤트 리스트)
view_value = "calendar"

# event number - 전체이벤트 리스트 시 빈칸
event_value = ""

# 장소
place_value = "617"

# 몇월
date_value = "202306"

formatted_url = url.format(view_value, event_value, place_value, date_value)

html = requests.get(formatted_url)
soup = BeautifulSoup(html.content, "html.parser")


# Find all div elements with class 'thumb_cont'
thumbnail_items = soup.find_all("div", class_="thumb_cont")

# Create a list to store the extracted information
event_info = []


for item in thumbnail_items:
    event_title = item.find(class_="tit").text.strip()
    event_date = item.find(class_="thumb_date").text.strip()
    event_num = item.find("a", onclick=True)["onclick"].split("'")[1]
    event_img = item.find("img")["src"]

    # Create a dictionary for the current item
    item_data = {
        "event_title": event_title,
        "event_date": event_date,
        "event_num": event_num,
        "event_img": event_img,
    }

    # Add the item data to the list
    event_info.append(item_data)

print(event_info)

# Save data as JSON
with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(event_info, json_file, ensure_ascii=False, indent=4)

print("Data saved as JSON.")


### JSON TO DB
import psycopg2
import json

# ...

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="db_gwolnadri",
    user="admin",
    password="admin",
)

# Create a cursor to execute SQL statements
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
    CREATE TABLE IF NOT EXISTS event_data (
        event_title VARCHAR,
        event_num VARCHAR,
        event_img VARCHAR,
        event_date VARCHAR
    )
"""
cursor.execute(create_table_query)

# Commit the changes to the database
conn.commit()

# ...

# Insert each item's data into the PostgreSQL database
for item_data in event_info:
    sql = "INSERT INTO event_data (event_title, event_num, event_img, event_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (
        item_data["event_title"],
        item_data["event_num"],
        item_data["event_img"],
        item_data["event_date"],
    ))

# ...

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data saved to PostgreSQL database.")
