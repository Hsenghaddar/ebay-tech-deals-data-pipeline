from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

URL = "https://www.ebay.com/globaldeals/tech"

def scroll_page():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_deals():
    driver.get(URL)
    time.sleep(5)
    scroll_page()

    products = driver.find_elements(By.CSS_SELECTOR, "div.dne-itemtile")

    data = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for product in products:
        try:
            title = product.find_element(By.CSS_SELECTOR, "h3").text
        except:
            title = ""

        try:
            price = product.find_element(By.CSS_SELECTOR, ".first").text
        except:
            price = ""

        try:
            original_price = product.find_element(By.CSS_SELECTOR, ".itemtile-price-strikethrough").text
        except:
            original_price = ""

        try:
            shipping = product.find_element(By.CSS_SELECTOR, ".dne-itemtile-delivery").text
        except:
            shipping = ""

        try:
            item_url = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            item_url = ""

        row = {
            "timestamp": timestamp,
            "title": title,
            "price": price,
            "original_price": original_price,
            "shipping": shipping,
            "item_url": item_url
        }

        data.append(row)

    return data

def save_to_csv(data):
    file_name = "ebay_tech_deals.csv"

    try:
        df = pd.read_csv(file_name)
    except:
        df = pd.DataFrame(columns=[
            "timestamp",
            "title",
            "price",
            "original_price",
            "shipping",
            "item_url"
        ])

    new_rows = pd.DataFrame(data)
    df = pd.concat([df, new_rows], ignore_index=True)
    df.to_csv(file_name, index=False)

if __name__ == "__main__":
    scraped = scrape_deals()

    if scraped:
        save_to_csv(scraped)        
    driver.quit()