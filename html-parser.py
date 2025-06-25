
import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

# Beispiel-URL (anpassen!)
BASE_URL = "https://www.autoscout24.de/angebote/mg-mg4-standard-sitz-lenkradhzg-carplay-mg-pilot-elektro-schwarz-8e835da7-2396-42f7-89bf-e14af4d3d702?sort=standard&desc=0&lastSeenGuidPresent=true&cldtidx=382&position=382&search_id=19y0owctbh3&standardSortStrategy=mia_ltr&source_otp=t50&ap_tier=t50&source=listpage_search-results&order_bucket=6&new_taxonomy_available=false&boosting_product=mia&relevance_adjustment=boost&applied_boost_level=t50&boost_level=t50"

# User-Agent simuliert echten Browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Liste für gesammelte Daten
data = []

url = BASE_URL
print(f"Scraping {url}")

# Liste von Cookies, welche von der Website benötigt werden, damit der Cookiebanner nicht angezeigt wird.
necessary_cookies = [
    {
        "name":     "_asse",
        "value":    "cm:eyJzbSI6WyIxfDE3NDg5MzgzMjgwMjd8MHwwfDB8biIsMTgxMjAxMDMyODAyN119",
        "secure":   False
    },
    {
        "name":     "_cq_duid",
        "value":    "1.1748938746.k917G3inM7mKC8Nh",
        "secure":   True
    },
    {
        "name":     "_cq_pxg",
        "value":    "3|6652109758",
        "secure":   True
    },
    {
        "name":     "_cq_suid",
        "value":    "1.1748938746.299na4GA431p7721",
        "secure":   True
    },
    {
        "name":     "addtl_consent",
        "value":    "1~",
        "secure":   False
    },
    {
        "name":     "as24-cmp-signature",
        "value":    "L%2BmhqL7G7PwLQWoFaJYzr9mAGTvG9Xdndl3tNFDEccicI4NjOFbBwsKevt3xnBPL%2F292Q3ORYs5VXs44zk3n%2BN4qOy4QahDz8gSkS2v%2BPWIFm7oyJqj9x6tRx9ikzjh0mIRJu8%2FIiqj6K4%2FyPtnQQO1IVBIAWOXf9a6iFQX0Mbs%3D",
        "secure":   False
    },
    {
        "name":     "as24Visitor",
        "value":    "ca813bb2-ddcd-4568-8240-40426ec50860",
        "secure":   False
    },
    {
        "name":     "cconsent-v2",
        "value":    "%7B%22purpose%22%3A%7B%22legitimateInterests%22%3A%5B25%5D%2C%22consents%22%3A%5B%5D%7D%2C%22vendor%22%3A%7B%22legitimateInterests%22%3A%5B10218%2C10441%2C11006%2C11005%2C11019%5D%2C%22consents%22%3A%5B%5D%7D%7D",
        "secure":   False
    },
    {
        "name":     "euconsent-v2",
        "value":    "CQSbk4AQSbk4AGNAGCDEBjFgAAAAAAAAAAAAAAAAAADBIEQACwAKgAcAA8ACCAF4AaAA8ACYAFUAN4AfgBCQCGAIkARwAmgBhgDLAHOAO4Ae0A_AD9AI4ASUBIgChwFHgKRAWwAuQBkgDMwGrgQhAoQOgUgALAAqABwAEEALwA0AB4AEwAKYAVQAugBiADeAH6AQwBEgCOAE0AKMAYYA0QBzgDuAHtAPwA_QCLQEcAR0AkoB1AEXgJEATIAocBR4C2AFyAMkAZUAywBmYDVwHFgUIIQCgAFgBVADEAG8Ac4A7gCOAEpAOoAuQlATAAWABwAHgATAAqgBigEMARIAjgBRgD8AI4AdQBF4CRAFHgLYAZIAywCEJSA4AAsACoAHAAQQAyADQAHgATAAqgBiAD9AIYAiQBHACjAGiAOeAfgB-gEWgI4AjoBJQDqAIvASIAocBbAC5AGSAMsAhCWgCADuAI4AocBmYAAA.cAAAAAAAA4CA",
        "secure":   False
    },
]
# In ein Dictionary umwandeln, da requests keine Liste akzeptiert:
cookies_dict = {cookie["name"]: cookie["value"] for cookie in necessary_cookies}

# Request senden
response = requests.get(url, headers=HEADERS, cookies=cookies_dict)
if response.status_code != 200:
    print(f"Fehler beim Laden: {response.status_code}")

# HTML parsen
soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
price_span = soup.find("span", class_="PriceInfo_price__XU0aF")

with open("tmp.txt", "w", encoding="utf-8") as f:
    f.write(txt)
    f.close()

# Zufällige Pause (Bot-Erkennung vermeiden)
time.sleep(random.uniform(1.5, 4.0))

# In DataFrame umwandeln & speichern
df = pd.DataFrame(data)
df.to_csv("scraped_data.csv", index=False)
print("Scraping abgeschlossen.")
