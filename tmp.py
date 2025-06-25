import json

with open("car_urls.txt", "r", encoding="utf-8") as f:
    urls = json.load(f)
    print(len(urls))