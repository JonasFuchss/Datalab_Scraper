import selenium
import json
import os
import random
import pandas as pd
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webelement import WebElement
from pandas.core.frame import DataFrame
from selenium.webdriver.remote.webelement import WebElement
from tokenize import String
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser_path = "/usr/bin/firefox"

result_dataframe: DataFrame = pd.DataFrame()


def main() -> None:
    options = Options()
    options.headless = False

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

    # Geckodriver ermöglicht das Kommunizieren mit Firefox über Python
    gecko_path = "/usr/bin/geckodriver"

    # Webdriver initialisieren
    service = Service(gecko_path)
    driver = webdriver.Firefox(service=service, options=options)

    # Wenn es bereits gescrapdte URLs / Städte gibt, lese die vorher ein.
    if os.path.exists("car_urls.txt"):
        with open("car_urls.txt", "r", encoding="utf-8") as f:
            car_urls = json.load(f)
            f.close()
    else:
        print("keine Datei mit Car-URLs vorhanden. Erstelle neue leere.")
        car_urls: list = []
    if os.path.exists("scraped_cities.txt"):
        with open("scraped_cities.txt", "r", encoding="utf-8") as f:
            scraped_cities = json.load(f)
            f.close
    else:
        scraped_cities = []
        print("keine Datei mit gescrapten Städten vorhanden. Erstelle neue leere.")

    try:
        stadt_urls: list[str] = []

        # Zielseite aufrufen
        url = "https://www.autoscout24.de/auto/gebrauchtwagen/"
        driver.get(url)

        # Nach dem ersten Aufruf der Website alle Cookies hinzufügen und danach einmal refreshen
        for cookie in necessary_cookies:
            driver.add_cookie(cookie)
        driver.refresh()

        # Wenn die Stadt-URLs schon in der Datei existieren lese die URLs einfach nur aus. Sonst: Scrape neu.
        try:
            with open("city_urls.txt", "r", encoding="utf-8") as f:
                stadt_urls = json.load(f)
                f.close()
        except FileNotFoundError:
            print("Keine Datei mit Stadt-URLs gefunden. Scrape neu.")
            bundesland_urls = []

            # Suche die Deutschlandkarte raus und speichere alle darin enthaltenen URLs der Bundesländer zwischen.
            element = read_out_element(driver, By.ID, "Deutschland", 5.0)
            bundesland_elements = element.find_elements(By.TAG_NAME, "a")
            for e in bundesland_elements:
                bundesland_urls.append(e.get_attribute("xlink:href"))
            print(bundesland_urls)

            # Rufe hintereinander alle Bundesländer auf und schreibe aus jedem alle Städte-Links raus
            # Da bestimmte Bundesländer (wie Berlin) sofort Autos anzeigen, wird erst getestet, ob das der Fall ist.
            # Wenn ja, wird die Bundesland URL auch direkt zu den Städten hinzugefügt
            for bundesland_url in bundesland_urls:
                wait_random()
                driver.get(bundesland_url)
                if check_for_element(driver, By.CLASS_NAME, "opt-rank-list-section"):
                    element = read_out_element(driver, By.XPATH, "/html/body/div/div[2]/div[4]/ol")
                    stadt_elements = element.find_elements(By.TAG_NAME, "li")
                    for e in stadt_elements:
                        stadt_urls.append(e.find_element(By.TAG_NAME, "a").get_attribute("href"))
                else:
                    stadt_urls.append(bundesland_url)
                print(str(stadt_urls) + "\n--------------")

            # Speichere alle Stadt-URLs zwischen in eine txt-Datei
            with open("city_urls.txt", mode="w", encoding="utf-8") as f:
                json.dump(stadt_urls, f, ensure_ascii=False)
                f.close()

        # Nachdem die URLs aller Städte ausgelesen wurden, rufe hintereinander alle Städte auf
        for stadt_url in stadt_urls:
            scraped_url_count = 0
            double_url_count = 0
            failed_scrapes_count = 0

            print(f"************\nVersuche, {stadt_url} zu scrapen")

            # Wurde die Stadt bereits schon mal gescraped? Wenn ja, überspringe sie.
            if stadt_url in scraped_cities:
                print("wurde schon mal gescraped, überspringe daher.")
                continue

            wait_random()
            driver.get(stadt_url)

            # Rufe "alle Angebote anzeigen" für die jeweilige Stadt auf
            element = read_out_element(driver, type=By.LINK_TEXT, element_identifier="Alle Angebote anzeigen")
            driver.get(element.get_attribute("href"))

            # schaue, wie viele Seiten (max 20) die Stadt hat und hole dir die URLs von allen Autos aus allen Seiten
            page_navigator_bar: WebElement = read_out_element(driver, type=By.CSS_SELECTOR, element_identifier=".scr-pagination.FilteredListPagination_pagination__3WXZT")
            pages: list[WebElement] = page_navigator_bar.find_elements(By.CSS_SELECTOR, ".pagination-item")
            page_count: int = int(pages[len(pages)-1].text)

            for p in range(page_count):
                wait_random(1.0)
                print("Scraping Page " + str(p+1))
                main_row_element = read_out_element(driver, type=By.CSS_SELECTOR, element_identifier=".ListPage_main___0g2X")
                entries = main_row_element.find_elements(By.TAG_NAME, "article")
                for e in entries:
                    try:
                        url = e.find_element(By.TAG_NAME, "a").get_attribute("href")
                        if url not in car_urls:
                            car_urls.append(url)
                            scraped_url_count += 1
                        else:
                            double_url_count += 1
                    except:
                        print(f"Scrape fehlgeschlagen. Überspringe nach kurzem Delay.")
                        wait_random(max=1.5)
                        failed_scrapes_count += 1
                
                # Speichere alle bisherigen URLs zwischen, um bei einem Block Fortschrittverlust zu verhindern.
                with open("car_urls.txt", mode="w", encoding="utf-8") as f:
                    json.dump(car_urls, f, ensure_ascii=False)
                    f.close()

                if p+1 != page_count:
                    next_page_button = read_out_element(driver, By.CSS_SELECTOR, element_identifier="[aria-label='Zu nächsten Seite']")
                    next_page_button.click()
            
            print(f"+++++++++++\nStadt wurde vollständig gescraped, mit {scraped_url_count + double_url_count} neuen Einträgen.\n{double_url_count} URLs davon waren schon bekannt und wurden daher übersprungen.\n{failed_scrapes_count} Scrapes sind fehlgeschlagen.")

            # wenn eine Stadt komplett gescraped wurde, speichere die Stadt in einer Separaten Datei zwischen.
            scraped_cities.append(stadt_url)
            with open("scraped_cities.txt", mode="w", encoding="utf-8") as f:
                json.dump(scraped_cities, f, ensure_ascii=False)
                f.close()



            

    finally:
        # Graceful shutdown
        driver.quit()


def check_for_element(driver: webdriver.Firefox, type: By, element_identifier: str, timeout: float = 20.0) -> bool:
    """
    Prüft, ob ein spezifiziertes Element im DOM vorhanden ist.

    Parameters
    ----------
    driver : webdriver.Firefox
        Die Driver-Instanz von Firefox
    type : By
        Der Typ des Identifiers, auf welchen getestet werden soll
    element_identifier : str
        Der eindeutige Identifier, welcher gesucht wird
    timeout : float
        Die Zeit in Sekunden, welche das zu suchende Element maximal laden darf, bevor es als "nicht existierend" zurückgegeben wird, by default 20.0

    Returns
    -------
    bool
        Ob das Element mit dem Identifier im DOM existiert
    """
    try:
        # Prüfe auf das Element
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((type, element_identifier)))
        return True
    except Exception as e:
        return False


def read_out_element(driver: webdriver.Firefox, type: By, element_identifier: str, timeout: float = 20.0) -> WebElement:
    """
    Hilfsfunktion, welche wartet, bis ein Element im DOM geladen ist und daraufhin das Element über den type und identifier zurückgibt.

    Parameters
    ----------
    driver : webdriver.Firefox
        Die Instanz des Firefox-Webdrivers, welcher die Webseite anspricht
    type : By
        Typ des Elements.
    element_identifier : str
        Abhängig vom Typ der String, mit welchem das Element im DOM identifiziert werden kann.
    timeout : float, optional
        Wie lange die Funktion maximal das Laden des Elements erwartet in Sekunden. Wird das Element nicht rechtzeitig geladen oder existiert nicht, wird eine TimeoutException geworfen, by default 20.0

    Returns
    -------
    WebElement
        das erste, gefundene Element.

    Raises
    ------
    TimeoutException
        Falls das Element nicht innerhalb des Timeout-Limits gefunden wird.
    """
    try:
        # Warte bis das Element geladen ist und versuch es dann auszulesen
        wait = WebDriverWait(driver, timeout)
        element: WebElement = wait.until(EC.presence_of_element_located((type, element_identifier)))
        return element
    except Exception as e:
        raise e


def wait_random(min: float = 0.5, max: float = 3.0) -> None:
    """
    Legt den Scraper für eine zufällige Zeit lang schlafen, um automatische Blockung durch zu viele, schnell aufeinanderfolgende Abfragen vorzubeugen

    Parameters
    ----------
    min : float, optional
        die minimale Wartezeit in Sekunden, by default 0.5
    max : float, optional
        die maximale Wartezeit in Sekunden, by default 3.0
    """
    delay = random.uniform(a = min, b = max)
    time.sleep(delay)





######################
######################
### Autoausführung ###
######################
######################


if __name__ == "__main__":
    main()