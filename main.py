from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
def read_root():
    response = requests.get("http://118.155.207.14/self-study/")
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    data_list = []

    for table in soup.find_all("table", attrs={"class": "table"}):
        
        tr_list = table.find("tbody").find_all("tr")
        data = {
            "date": table.find("caption").text.replace(" ", ""),
            "timetable": []

        }
        
        for tr in tr_list:
            timetable_list = [[ content.string for content in td.contents if content.string is not None and content != "\xa0" ] for td in tr.find_all("td")]
            data["timetable"].append({
                "no": tr.find("th").text.replace("\xa0", ""),
                "available": timetable_list[1],
                "noAvailable": timetable_list[0]
            })
        data_list.append(data)

    return {
        "lastUpdated": soup.find(id="last-update").text.replace("最終更新：", ""),
        "data": data_list,
    }
