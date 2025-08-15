import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Load filters and targets
with open("filters.json") as f:
    FILTERS = json.load(f)
with open("targets.json") as f:
    TARGETS = json.load(f)

# Load secrets from Replit environment
PROFILE = {
    "name": os.environ['FULL_NAME'],
    "email": os.environ['EMAIL'],
    "address": os.environ['ADDRESS'],
    "city": os.environ['CITY'],
    "zip": os.environ['ZIP'],
    "payment": os.environ['PAYMENT_METHOD'],
    "repayment_platform": os.environ['REPAYMENT_PLATFORM'],
    "repayment_account": os.environ['REPAYMENT_ACCOUNT']
}
API_KEYS = {
    "stockx": os.environ['STOCKX_API_KEY'],
    "artstation": os.environ['ARTSTATION_API_KEY'],
    "graphicriver_user": os.environ['GRAPHICRIVER_USERNAME'],
    "graphicriver_pass": os.environ['GRAPHICRIVER_PASSWORD'],
    "deviantart": os.environ['DEVIANTART_API_KEY']
}

REPAID = False
REPAY_AMOUNT = 100.00
profit_total = 0.00

def start_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    return webdriver.Chrome(options=opts)

def buy_product(driver, target):
    driver.get(target["url"])
    try:
        driver.find_element(By.XPATH, target["add"]).click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, target["checkout"]).click()
        driver.find_element(By.NAME, "name").send_keys(PROFILE["name"])
        driver.find_element(By.NAME, "email").send_keys(PROFILE["email"])
        driver.find_element(By.NAME, "address").send_keys(PROFILE["address"])
        driver.find_element(By.NAME, "city").send_keys(PROFILE["city"])
        driver.find_element(By.NAME, "zip").send_keys(PROFILE["zip"])
        driver.find_element(By.NAME, "payment").send_keys(PROFILE["payment"])
        driver.find_element(By.XPATH, "//button[contains(text(),'Place Order')]").click()
        print(f"Purchased: {target['title']}")
        return True
    except Exception as e:
        print(f"Failed purchase: {target['title']}")
        return False

def payout(amount):
    global profit_total, REPAID
    if not REPAID:
        if profit_total >= REPAY_AMOUNT:
            print(f"Sending ${REPAY_AMOUNT} to {PROFILE['repayment_platform']} account {PROFILE['repayment_account']}")
            REPAID = True
        else:
            print(f"Continuing repayment. Current: ${profit_total}")
    else:
        print(f"Sending ${amount} to YOUR account.")

while True:
    driver = start_driver()
    for target in TARGETS:
        if buy_product(driver, target):
            # Simulated profit increment for testing
            profit_total += (target["sell_price"] - 5)  
            payout(profit_total)
    driver.quit()
    time.sleep(60)
