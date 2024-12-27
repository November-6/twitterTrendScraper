from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options

import time
import uuid
from datetime import datetime

from db import client


db = client.flask_database
collection = db.collection


MONGODB_URI = 'mongodb+srv://nayaa3231:<bWmgxZgpyEHaxFYA>@internproject.flgvh.mongodb.net/?retryWrites=true&w=majority&appName=internproject'



def scrape_twitter():
    options = webdriver.FirefoxOptions()
    #options.headless = True  # Disable headless for debugging
    options.add_argument("-headless")  # Attempt to bypass bot detection
    #options.add_argument("--disable-blink-features")
    #options.add_argument("--disable-blink-features=AutomationControlled")  # Attempt to bypass bot detection

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

        # Wait for either email or password input field
        try:
            # Check for the email field first
            email_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            email_input.send_keys("abhinavprajapati589@gmail.com")
            email_input.send_keys(Keys.RETURN)
            print("Email entered")
        except:
            # If no email field, proceed to check for the password field
            pass

        # Wait for password input to appear
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        # Enter password
        password_input.send_keys("Abhinav@2004")
        password_input.send_keys(Keys.RETURN)
        print("Password entered")

        # Wait for the home page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Fetch trending topics by locating elements
        try:
            # Use a more comprehensive CSS selector for all trending items (hashtags and phrases)
            trending_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now'] span[dir='ltr'], div[aria-label='Timeline: Trending now'] div[dir='ltr']"))
            )
            
            
          

            # Extract trending topics (both hashtags and phrases)
            # Extract trending topics (both hashtags and phrases)
            # Extract trending topics (both hashtags and phrases)
            # Extract trending topics (both hashtags and phrases)
            trending_topics = []
            for element in trending_elements:
                try:
                    topic_name = element.text
                    # Ensure only valid topics are added: exclude irrelevant ones like categories or post counts
                    if topic_name and topic_name not in ["What’s happening", "Show more"] and not any(char.isdigit() for char in topic_name):
                        # Exclude category/region labels (e.g., "Politics · Trending", "Entertainment · Trending")
                        if "Trending" not in topic_name and "·" not in topic_name:
                            if topic_name not in trending_topics:  # Avoid duplicates
                                trending_topics.append(topic_name)
                except Exception as e:
                    print(f"Error extracting topic: {e}")
                    continue

            # Print and save filtered trending topics to the database with unique ID and timestamp
            print("Filtered Trending Topics:", trending_topics)
            data = {
                "trending_topics": trending_topics,
                "timestamp": datetime.utcnow(),  # Store timestamp in UTC
                "unique_id": str(uuid.uuid4())  # Generate a unique ID for each entry
            }
            print(data)
            db.collections.insert_one(data)




            return {
                "status": "success",
                "message": "Login and trending topics fetched successfully",
                "trending_topics": trending_topics
            }

        except Exception as e:
            print(f"Error fetching trending topics: {e}")
            return {
                "status": "error",
                "message": f"Error fetching trending topics: {str(e)}"
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        # Ensure the driver quits after execution
        time.sleep(10)
        driver.quit()

# Call the scrape function
