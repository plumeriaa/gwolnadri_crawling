import requests
from bs4 import BeautifulSoup
import json

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

data = {}

for item in list_items:
    span = item.find("span")
    if span is not None:
        span_text = span.text.strip()
        try:
            p_text = item.find("p").text.strip()
        except AttributeError:
            p_text = ""
        data[span_text] = p_text

event_title = soup.find(class_="link_tit").text.strip()
event_dates = data.get("기간", "")
event_time = data.get("시간", "")
event_place = data.get("장소", "")
book_date = data.get("예매기간", "")
book_time = data.get("예매시간", "")
event_price = data.get("가격", "")
event_booking = data.get("신청", "")
event_inquiry = data.get("문의", "")

print("행사:", event_title)
print("기간:", event_dates)
print("시간:", event_time)
print("장소:", event_place)
print("예매기간:", book_date)
print("예매시간:", book_time)
print("가격:", event_price)
print("신청:", event_booking)
print("문의:", event_inquiry)

item_data = {
    "행사": event_title,
    "기간": event_dates,
    "시간": event_time,
    "장소": event_place,
    "예매기간": book_date,
    "예매시간": book_time,
    "가격": event_price,
    "신청": event_booking,
    "문의": event_inquiry,
}

data = item_data

# Save data as JSON
with open("data2.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Data saved as JSON.")
