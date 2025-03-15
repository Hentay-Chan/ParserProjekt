import requests
import json
import datetime
from bs4 import BeautifulSoup

class Parser:
    def __init__(self, url: str):
        self.url = url

    def fetch_page(self):
        response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            self.html = response.text
            self.soup = BeautifulSoup(self.html, "html.parser")
        else:
            raise Exception(f"Error: {response.status_code} while fetching the page")

    def parse(self):
        if not self.soup:
            raise Exception("Page has not been loaded yet. Use fetch_page().")
        
        broshurs = []

        for broshur in self.soup.find_all("div", class_="brochure-thumb"):
            title = broshur.find("strong").text
            thumbnail = broshur.find("img").get("src") or broshur.find("img").get("data-src")
            shop_name = broshur.find("img", class_="lazyloadLogo")["alt"].split(" ")[1]
            date_from_to = broshur.find("small", class_="hidden-sm").text.split(" ")
            try:
                datetime.datetime.strptime(date_from_to[0], "%d.%m.%Y")
                valid_from = date_from_to[0]
            except ValueError:
                valid_from = date_from_to[0] + " " + date_from_to[1]
            valid_to = date_from_to[-1]
            parsed_time =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            broshurs.append({
                "title": title, 
                "thumbnail": thumbnail,
                "shop_name": shop_name,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "parsed_time": parsed_time
            })
        return broshurs

    def save_to_file(self, filename: str, content):
        if not content:
            raise Exception("No HTML content to save. Use parse().")
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(content, file, indent=4, ensure_ascii=False)
        print(f"Brochures data saved to {filename}")

if __name__ == "__main__":
    url = "https://www.prospektmaschine.de/hypermarkte/"
    parser = Parser(url)
    
    try:
        parser.fetch_page()
        content = parser.parse()
        parser.save_to_file("save_parse.json", content)
    except Exception as e:
        print("Error:", e)
