import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import re
import random
import logging
import json
from tqdm.asyncio import tqdm
from fake_useragent import UserAgent
import os

# === Logging ===
LOG_FILE = "scraper.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === Config ===
SAVE_EVERY = 50
OUTPUT_FILE = "output.csv"
SUCCESS_FILE = "successfully_scraped_URLs.txt"

ua = UserAgent()
sem = asyncio.Semaphore(10)

BOX_IDS = [
    "basic-details-section",
    "listing-history-section",
    "technical-details-section",
    "environment-details-section",
    "equipment-section",
    "color-section"
]

necessary_cookies = {
    # deine Cookies hier
}

def extract_plz(a_element):
    if a_element and a_element.find('br'):
        parts = list(a_element.stripped_strings)
        plz_ort = parts[2]
    else:
        plz_ort = a_element.get_text(strip=True) if a_element else ""
    match = re.match(r'(\d{5})', plz_ort)
    return match.group(1) if match else None


def get_data_from_table(soup, table_class, table_column_class, table_row_class, existing_data):
    def extract_from_dl(data_dl):
        dt_elements = data_dl.find_all("dt", class_=table_column_class)
        dd_elements = data_dl.find_all("dd", class_=table_row_class)

        for dt, dd in zip(dt_elements, dd_elements):
            key = dt.get_text(strip=True)
            ul = dd.find("ul")
            if ul:
                for li in ul.find_all("li"):
                    li_text = li.get_text(strip=True)
                    existing_data[li_text] = True
            else:
                if dd.find_all("p"):
                    continue
                else:
                    value = dd.get_text(strip=True)
                    existing_data[key] = value

    all_data_dl = soup.find_all("dl", class_=table_class)
    for data_dl in all_data_dl:
        extract_from_dl(data_dl)

    hidden_containers = soup.find_all(attrs={"aria-hidden": "true"})
    for container in hidden_containers:
        hidden_dls = container.find_all("dl", class_=table_class)
        for hidden_dl in hidden_dls:
            extract_from_dl(hidden_dl)


async def fetch_html(session, url):
    headers = {"User-Agent": ua.random}
    async with sem:
        try:
            async with session.get(url, headers=headers, cookies=necessary_cookies) as response:
                await asyncio.sleep(random.uniform(1.0, 3.0))
                if response.status != 200:
                    logging.warning(f"[{url}] Fehler {response.status}")
                    return None
                return await response.text()
        except Exception as e:
            logging.error(f"[{url}] Verbindungsfehler: {e}")
            return None


async def scrape_url(session, url):
    logging.info(f"[{url}] Scraping gestartet")
    html = await fetch_html(session, url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    result_dict = {}

    # result_dict["URL"] = url

    title_field = soup.find("span", class_="StageTitle_boldClassifiedInfo__sQb0l StageTitle_textOverflow__KN9BA")
    if title_field:
        result_dict["Titel"] = title_field.get_text(strip=True)

    price_field = soup.find("span", class_="PriceInfo_price__XU0aF")
    if price_field:
        try:
            result_dict["Preis"] = int(price_field.get_text(strip=True).split(sep="€ ")[1].replace(".", ""))
        except:
            result_dict["Preis"] = None

    seller_field = soup.find("span", class_="scr-tag scr-tag--default")
    if seller_field:
        result_dict["Verkaufsart"] = seller_field.get_text(strip=True)

    seller_location_field = soup.find("a", class_="scr-link Department_link__xMUEe")
    plz = extract_plz(seller_location_field)
    if plz:
        result_dict["Verkaufsort"] = plz

    for id in BOX_IDS:
        box = soup.find(id=id)
        if box:
            get_data_from_table(
                box,
                "DataGrid_defaultDlStyle__xlLi_",
                "DataGrid_defaultDtStyle__soJ6R",
                "DataGrid_defaultDdStyle__3IYpG",
                result_dict
            )

    logging.info(f"[{url}] {len(result_dict)} Datenpunkte extrahiert")
    return result_dict


async def scrape_all(urls):
    scraped_data = []
    completed = load_completed_urls()

    urls_to_scrape = [url for url in urls if url not in completed]
    total = len(urls_to_scrape)

    if total == 0:
        logging.info("Keine neuen URLs zu scrapen.")
        return

    logging.info(f"{total} URLs werden gescraped.")
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls_to_scrape):
            tasks.append(scrape_url(session, url))

            if len(tasks) >= SAVE_EVERY or i == total - 1:
                batch_results = await asyncio.gather(*tasks)
                batch_results = [r for r in batch_results if r]

                scraped_data.extend(batch_results)
                save_results(scraped_data, OUTPUT_FILE)
                scraped_data.clear()

                write_success_urls([urls_to_scrape[j] for j in range(i + 1 - len(tasks), i + 1)])
                logging.info(f"Zwischenspeicherung nach {i + 1} URLs abgeschlossen.")
                tasks.clear()


def save_results(data, filename):
    df_new = pd.DataFrame(data)
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename, low_memory=False)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(filename, index=False, encoding="utf-8")
    logging.info(f"{len(df_new)} neue Einträge gespeichert ({len(df_combined)} insgesamt).")


def write_success_urls(urls):
    with open(SUCCESS_FILE, "a", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")


def load_completed_urls():
    if os.path.exists(SUCCESS_FILE):
        with open(SUCCESS_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def main():
    with open("car_urls.txt", "r", encoding="utf-8") as f:
        urls: list = json.load(f)

    asyncio.run(scrape_all(urls))
    logging.info("Scraping abgeschlossen.")

if __name__ == "__main__":
    main()
