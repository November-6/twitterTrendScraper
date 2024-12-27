import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
import requests
import pymongo
import uuid
import datetime
import os

USERNAME = "abhinavp798777"  # Set your Twitter username in environment variables
PASSWORD = "Abhinav@2004"  # Set your Twitter password in environment variables
PROXYMESH_USER = os.getenv("PROXYMESH_USER")  # Set ProxyMesh username
PROXYMESH_PASS = os.getenv("PROXYMESH_PASS") 

chrome_driver_path = r"C:\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)
options = Options()

options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flag
options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flag

#options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flag
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")  
options.headless = True

# Secure credentials

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://x.com/i/flow/login")
print(driver.title)
wait = WebDriverWait(driver, 150)

try:
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
    username_input.click()
    username_input.send_keys(USERNAME)
    time.sleep(5)
    username_input.send_keys(Keys.RETURN)
except Exception as e:
    print(f"Error: {e}")

# Wait for Password Field
password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))

password_input.click()
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.RETURN)
