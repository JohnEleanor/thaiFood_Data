import requests
from bs4 import BeautifulSoup
import time
import re

# URL หลักของเว็บ
base_url = "https://inmu2.mahidol.ac.th/thaifcd/search_food_by_name.php"

# ใช้ requests session เพื่อให้ประสิทธิภาพดีขึ้น
session = requests.Session()

# ส่งคำขอไปที่เว็บเพื่อดึงหน้าเพจ
response = session.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# ค้นหาลิงก์ที่มี food_id
food_links = []
for link in soup.select("a[href^='search_food_by_name_result.php?food_id=']"):
    food_id = link["href"].split("=")[-1]
    food_links.append(food_id)

print(f"พบรายการอาหารทั้งหมด {len(food_links)} รายการ")


import json

# # ฟังก์ชันดึงข้อมูลสารอาหารของอาหารแต่ละชนิด
# def scrape_food_data(food_id):
#     food_url = f"https://inmu2.mahidol.ac.th/thaifcd/search_food_by_name_result.php?food_id={food_id}"
    
#     response = session.get(food_url)
#     response.encoding = "tis-620"  # หรือ 'windows-874' แล้วแต่กรณี
#     soup = BeautifulSoup(response.text, "html.parser")

#     # เก็บข้อมูลอาหาร
#     food_data = {"food_id": food_id, "url": food_url}

#     # ดึงชื่ออาหาร
#     name_tag = soup.find("h1")
#     if name_tag:
#         food_data["name"] = name_tag.text.strip()

#     # ดึงข้อมูลจากข้อความที่มีการแยกด้วย "Food Code:"
#     food_details_text = soup.get_text()
    
#     # ใช้ Regular Expression เพื่อดึง Food Code, Thai name, English name และ Scientific name
#     match_food_code = re.search(r"Food Code:\s*([^\n]+)", food_details_text)
#     match_thai_name = re.search(r"Thai name:\s*([^\n]+)", food_details_text)
#     match_eng_name = re.search(r"English name:\s*([^\n]+)", food_details_text)
#     if match_food_code:
#         food_data["Food_Code"] = match_food_code.group(1)
#         food_data["Thai_name"] = match_thai_name.group(1)
#         food_data["English_name"] = match_eng_name.group(1)


#         # กำหนดข้อมูลที่จะส่ง
#         data = {
#             'mode': 'BRANDEDFOOD_NUTRIENT_LOAD',
#             'food_id': '1009',
#             'nutrient_name': '',
#             'value_per_servingsize': '1',
#             'value_per_100g': '1'
#         }

#         # ทำการโพสต์คำขอ
#         response2 = session.post('https://inmu2.mahidol.ac.th/thaifcd/search_food_by_name__ajax_function.php', data=data)

#         # แปลงเนื้อหาของการตอบกลับเป็น BeautifulSoup
#         soup2 = BeautifulSoup(response2.text, "html.parser")

#         # หา div ที่มี class เป็น divTableRow
#         rows = soup2.find_all("div", class_="divTableRow")

#         # สร้าง dictionary เพื่อเก็บข้อมูล
#         nutrition_data = {}

#         # สำหรับแต่ละแถวในตาราง
#         for row in rows:
#             cells = row.find_all("div", class_="divTableCell")
#             if len(cells) == 3:
#                 nutrient_name = cells[0].text.strip()  # ชื่อสารอาหาร
#                 unit = cells[1].text.strip()           # หน่วย
#                 value = cells[2].text.strip()          # ค่า

#                 if nutrient_name == "Energy, by calculation":
#                     nutrient_name = "food_calories"
#                 elif (nutrient_name == "Protein, total"):
#                     nutrient_name = "food_protein"
#                 elif (nutrient_name == "Fat, total"):
#                     nutrient_name = "food_fat"
#                 elif (nutrient_name == "Carbohydrate, available"):
#                     nutrient_name = "food_carbohydrate"

#                 # เพิ่มข้อมูลลงใน dictionary
#                 nutrition_data[nutrient_name] = {"unit": unit, "value": value}

#                 food_data["nutrition"] = nutrition_data

      
  

#     return food_data



# # วนลูปดึงข้อมูลอาหารสำหรับ food_id ตั้งแต่ 1 ถึง 2000
# all_food_data = []
# for food_id in range(1, 2073):
#     print(f"Get Food Data ID {food_id}...")
#     data = scrape_food_data(food_id)
#     all_food_data.append(data)
#     # time.sleep(0.5)  # หน่วงเวลาเพื่อไม่ให้เซิร์ฟเวอร์โดนโหลดหนักเกินไป


# ฟังก์ชันดึงข้อมูลสารอาหารของอาหารแต่ละชนิด
def scrape_food_data(food_id):
    food_url = f"https://inmu2.mahidol.ac.th/thaifcd/search_food_by_name_result.php?food_id={food_id}"
    
    response = session.get(food_url)
    response.encoding = "tis-620"  # หรือ 'windows-874' แล้วแต่กรณี
    soup = BeautifulSoup(response.text, "html.parser")

    # เก็บข้อมูลอาหาร
    food_data = {"food_id": food_id, "url": food_url}

    # ดึงชื่ออาหาร
    name_tag = soup.find("h1")
    if name_tag:
        food_data["name"] = name_tag.text.strip()

    # ดึงข้อมูลจากข้อความที่มีการแยกด้วย "Food Code:"
    food_details_text = soup.get_text()
    
    # ใช้ Regular Expression เพื่อดึง Food Code, Thai name, English name และ Scientific name
    match_food_code = re.search(r"Food Code:\s*([^\n]+)", food_details_text)
    match_thai_name = re.search(r"Thai name:\s*([^\n]+)", food_details_text)
    match_eng_name = re.search(r"English name:\s*([^\n]+)", food_details_text)
    if match_food_code:
        food_data["Food_Code"] = match_food_code.group(1)
        food_data["Thai_name"] = match_thai_name.group(1)
        food_data["English_name"] = match_eng_name.group(1)

        # กำหนดข้อมูลที่จะส่ง
        data = {
            'mode': 'BRANDEDFOOD_NUTRIENT_LOAD',
            'food_id': food_id,  # ใช้ food_id ของตัวเอง
            'nutrient_name': '',
            'value_per_servingsize': '1',
            'value_per_100g': '1'
        }

        # ทำการโพสต์คำขอ
        response2 = session.post('https://inmu2.mahidol.ac.th/thaifcd/search_food_by_name__ajax_function.php', data=data)

        # แปลงเนื้อหาของการตอบกลับเป็น BeautifulSoup
        soup2 = BeautifulSoup(response2.text, "html.parser")

        # หา div ที่มี class เป็น divTableRow
        rows = soup2.find_all("div", class_="divTableRow")

        # สร้าง dictionary เพื่อเก็บข้อมูล
        nutrition_data = {}

        # สำหรับแต่ละแถวในตาราง
        for row in rows:
            cells = row.find_all("div", class_="divTableCell")
            if len(cells) == 3:
                nutrient_name = cells[0].text.strip()  # ชื่อสารอาหาร
                unit = cells[1].text.strip()           # หน่วย
                value = cells[2].text.strip()          # ค่า

                if nutrient_name == "Energy, by calculation":
                    nutrient_name = "food_calories"
                elif (nutrient_name == "Protein, total"):
                    nutrient_name = "food_protein"
                elif (nutrient_name == "Fat, total"):
                    nutrient_name = "food_fat"
                elif (nutrient_name == "Carbohydrate, available"):
                    nutrient_name = "food_carbohydrate"

                # เพิ่มข้อมูลลงใน dictionary
                nutrition_data[nutrient_name] = {"unit": unit, "value": value}

        # กำหนด nutrition_data ใน food_data เพียงครั้งเดียว
        food_data["nutrition"] = nutrition_data

    return food_data


# วนลูปดึงข้อมูลอาหารสำหรับ food_id ตั้งแต่ 1 ถึง 2000
all_food_data = []
for food_id in range(129, 2074):
    print(f"Get Food Data ID {food_id}...")
    data = scrape_food_data(food_id)
    all_food_data.append(data)
    # time.sleep(0.5)  # หน่วงเวลาเพื่อไม่ให้เซิร์ฟเวอร์โดนโหลดหนักเกินไป


# บันทึกข้อมูลเป็นไฟล์ JSON
with open("food_data.json", "w", encoding="utf-8") as f:
    json.dump(all_food_data, f, indent=4, ensure_ascii=False)

print("ดึงข้อมูลเสร็จเรียบร้อย!")