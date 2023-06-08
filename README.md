# gwolnadri_crawling

**event_list.py - 달별 전체 행사 리스트 가져오기.**
  - 행사 이름
  - 행사 코드 : 상세 페이지 보려면 필요해서 가져와야했음.
  - 행사 이미지 
  - event_list.json으로 저장해서 db에 저장. 
 
*** 다시 보니, 저장된걸 불러오는게 아니라 json으로 저장도하고 db에도 저장하는 식으로 되어있음. 필요시 수정가능.

--- 

**event_info.py - 행사 상세 페이지**
  - url에 행사 코드 넣어서 크롤링
  - 다른 상세 정보 가져오기
 - event_info.json으로 저장됨.
 - event_info.json을 불러와서, event_title & event_time 으로 매칭 시켜 나머지 상세 정보 기입. 
 

*** event_info 상세 내역은 현재는 행사 하나씩 불러오게 되어있기 때문에, 코드 넣어서 직접 돌려줘야 생성됨. 

---

**test.py - testing하는 파일.**
