from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from flask import request

# from selenium.webdriver.chrome.options import Options
from flask import render_template

import time
import uuid
from datetime import datetime

from db import client


db = client.flask_database
collection = db.collection


def scrape_twitter():
    options = webdriver.FirefoxOptions()
    # options.headless = True
    options.add_argument("-headless")
    # options.add_argument("--disable-blink-features")
    # options.add_argument("--disable-blink-features=AutomationControlled")  # Attempt to bypass bot detection

    driver = webdriver.Firefox(options=options)

    try:
        driver.get("https://x.com/i/flow/login")

        # Wait for username input to be visible and interactable
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_input.click()
        username_input.send_keys("KishoriCharles")
        username_input.send_keys(Keys.RETURN)
        print("Username entered")

        try:
            # it sometimes asks for email too so heres that
            email_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            email_input.send_keys("abhinavprajapati589@gmail.com")
            email_input.send_keys(Keys.RETURN)
            print("Email entered")
        except:
            pass

        # password time
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        password_input.send_keys("Abhinav@2004")
        password_input.send_keys(Keys.RETURN)
        print("Password entered")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # extracting elements
        try:
            trending_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        "div[aria-label='Timeline: Trending now'] span[dir='ltr'], div[aria-label='Timeline: Trending now'] div[dir='ltr']",
                    )
                )
            )

            # filtering trending topics
            trending_topics = []
            for element in trending_elements:
                try:
                    topic_name = element.text
                    if (
                        topic_name
                        and topic_name not in ["What’s happening", "Show more"]
                        and not any(char.isdigit() for char in topic_name)
                    ):
                        if "Trending" not in topic_name and "·" not in topic_name:
                            if topic_name not in trending_topics:
                                trending_topics.append(topic_name)
                except Exception as e:
                    print(f"Error extracting topic: {e}")
                    continue

            print("Filtered Trending Topics:", trending_topics)
            data = {
                "trending_topics": trending_topics,
                "timestamp": datetime.now(),
                "unique_id": str(uuid.uuid4()),
            }
            print(data)

            try:
                db.collections.insert_one(data)
            except Exception as e:
                print(f"Error saving data to database: {e}")

                return {
                    "status": "error",
                    "message": f"Error saving data to database: {str(e)}",
                    "timestamp": datetime.now(),
                    "ip": request.remote_addr,
                    "heres the data tho": trending_topics,
                }

            return {
                "status": "success",
                "message": "Login and trending topics fetched successfully and saved to database",
                "timestamp": datetime.now(),
                "ip": request.remote_addr,
                "trending_topics": trending_topics,
            }

        except Exception as e:
            print(f"Error fetching trending topics: {e}")
            return {
                "status": "error",
                "timestamp": datetime.now(),
                "ip": request.remote_addr,
                "message": f"Error fetching trending topics: {str(e)}",
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "status": "error",
            "timestamp": datetime.now(),
            "ip": request.remote_addr,
            "message": str(e),
        }
    finally:
        time.sleep(3)
        driver.quit()
