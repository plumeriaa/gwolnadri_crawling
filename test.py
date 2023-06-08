import requests
from bs4 import BeautifulSoup
import json
import psycopg2

url = "https://www.chf.or.kr/cont/{}/all/month/menu/363?thisPage=1&idx={}&searchCategory1=&searchCategory2={}&searchField=all&searchDate={}&weekSel=&searchText="

# view or calendar (개별 이벤트, 전체이벤트 리스트)
view_value = "view"

# event number - 전체이벤트 리스트 시 빈칸
event_value = "109087"

# 장소
place_value = "617"

# 몇월
date_value = "202306"

formatted_url = url.format(view_value, event_value, place_value, date_value)

html = requests.get(formatted_url)
soup = BeautifulSoup(html.content, "html.parser")

list_items = soup.select("div.board_view_info li")

event_info = {}

for item in list_items:
    category = item.find('span').text.strip()
    value = item.find('p').text.strip()
    event_info[category] = value

event_title = soup.find(class_="link_tit").text.strip()
event_info["행사"] = event_title

# Save data as JSON
with open("event_info.json", "w", encoding="utf-8") as json_file:
    json.dump(event_info, json_file, ensure_ascii=False, indent=4)

print("Data saved as JSON.")

### CHANGE JSON KEY TO ENGLISH ###
with open("event_info.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Define a mapping dictionary for key changes
key_mapping = {
    "기간": "event_date",
    "시간": "event_time",
    "장소": "event_place",
    "예매기간": "book_date",
    "예매시간": "book_time",
    "가격": "event_price",
    "신청": "event_booking",
    "문의": "event_inquiry",
    "행사": "event_title"
}

# Create a new dictionary with updated keys
updated_data = {}
for key, value in data.items():
    if key in key_mapping:
        new_key = key_mapping[key]
        updated_data[new_key] = value

# Convert the updated data back to JSON
updated_json_data = json.dumps(updated_data, ensure_ascii=False, indent=4)
print(updated_json_data)

with open("event_info.json", "w", encoding="utf-8") as json_file:
    json.dump(updated_data, json_file, ensure_ascii=False, indent=4)

print("Data saved as JSON.")

### JSON TO DB ###

# Load data from JSON
with open("event_info.json", "r", encoding="utf-8") as json_file:
    event_data = json.load(json_file)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="db_gwolnadri",
    user="admin",
    password="admin"
)

# Create a cursor to execute SQL statements
cursor = conn.cursor()

# Add the missing column 'event_time' to the event_data table
alter_table_query = """
    ALTER TABLE event_data 
    ADD COLUMN event_time VARCHAR,
    ADD COLUMN event_place VARCHAR,
    ADD COLUMN book_date VARCHAR,
    ADD COLUMN book_time VARCHAR,
    ADD COLUMN event_price VARCHAR,
    ADD COLUMN event_booking VARCHAR,
    ADD COLUMN event_inquiry VARCHAR;
"""
cursor.execute(alter_table_query)

# Prepare the data for the update query
event_title = event_data.get("event_title")
event_date = event_data.get("event_date")
event_time = event_data.get("event_time")
event_place = event_data.get("event_place")
book_date = event_data.get("book_date")
book_time = event_data.get("book_time")
event_price = event_data.get("event_price")
event_booking = event_data.get("event_booking")
event_inquiry = event_data.get("event_inquiry")

if event_title and event_date:
    # Check if the row already exists in the table
    select_query = """
        SELECT COUNT(*) FROM event_data
        WHERE event_title = %s AND event_date = %s;
    """
    cursor.execute(select_query, (event_title, event_date))
    row_count = cursor.fetchone()[0]

    if row_count > 0:
        # If the row exists, update it
        update_query = """
            UPDATE event_data
            SET event_time = %s,
                event_place = %s,
                book_date = %s,
                book_time = %s,
                event_price = %s,
                event_booking = %s,
                event_inquiry = %s
            WHERE event_title = %s
                AND event_date = %s;
        """
        cursor.execute(update_query, (
            event_time,
            event_place,
            book_date,
            book_time,
            event_price,
            event_booking,
            event_inquiry,
            event_title,
            event_date
        ))
    else:
        # If the row doesn't exist, insert a new row
        insert_query = """
            INSERT INTO event_data (event_title, event_date, event_time, event_place, book_date,
                                   book_time, event_price, event_booking, event_inquiry)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            event_title,
            event_date,
            event_time,
            event_place,
            book_date,
            book_time,
            event_price,
            event_booking,
            event_inquiry
        ))

# Commit the changes to the database
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
