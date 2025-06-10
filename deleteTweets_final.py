import os
import time
import datetime
import json
import sys
import io
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException

# ====== CONFIGURATION ======
MAX_TWEETS = 100
SLEEP_EVERY = 5        # tweets
SLEEP_SECONDS = 60     # seconds after every block
HEADLESS = True        # set to False for visible browser
# ============================

# Logging setup
def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{now}] {msg}"
    print(formatted)
    with open("delete_tweet_log.txt", "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

# Paths and env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_PATH = os.path.join(BASE_DIR, "cookies.json")
load_dotenv()
EMAIL = os.getenv("TWITTER_EMAIL")
USERNAME = os.getenv("TWITTER_USERNAME")
PASSWORD = os.getenv("TWITTER_PASSWORD")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Browser setup
options = webdriver.ChromeOptions()
if HEADLESS:
    options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# ===== AUTH =====
def save_cookies():
    with open(COOKIE_PATH, "w", encoding="utf-8") as f:
        json.dump(driver.get_cookies(), f, ensure_ascii=False, indent=2)
    log("Cookies saved.")

def manual_login_and_save_cookies():
    log("Manual login started...")
    driver.get("https://x.com/login")
    time.sleep(3)
    driver.find_element(By.NAME, 'text').send_keys(EMAIL + Keys.ENTER)
    time.sleep(3)
    try:
        driver.find_element(By.NAME, 'text').send_keys(USERNAME + Keys.ENTER)
        time.sleep(3)
    except:
        pass
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD + Keys.ENTER)
    time.sleep(5)
    if "login" in driver.current_url or "challenge" in driver.current_url:
        log("Manual login failed.")
        driver.quit()
        exit()
    log("Manual login successful.")
    save_cookies()

def login_with_cookies_or_fallback():
    if os.path.exists(COOKIE_PATH):
        try:
            log("Trying login with cookies...")
            driver.get("https://x.com/")
            with open(COOKIE_PATH, "r", encoding="utf-8") as f:
                for cookie in json.load(f):
                    try:
                        driver.add_cookie(cookie)
                    except:
                        pass
            driver.get("https://x.com/home")
            time.sleep(5)
            if "login" in driver.current_url:
                raise Exception("Login with cookies failed.")
            log("Logged in with cookies.")
        except Exception as e:
            log(f"Cookie login error: {e}")
            manual_login_and_save_cookies()
    else:
        manual_login_and_save_cookies()

# ===== TWEET ACTIONS =====
def go_to_profile():
    driver.get(f"https://x.com/{USERNAME}")
    time.sleep(5)

def delete_tweet(tweet_element, index):
    try:
        menu_button = tweet_element.find_element(By.XPATH, ".//button[@data-testid='caret']")
        driver.execute_script("arguments[0].click();", menu_button)
        time.sleep(1.5)

        delete_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='menuitem']//span[text()='Delete']"))
        )
        delete_btn.click()
        time.sleep(1.5)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='confirmationSheetDialog']"))
        )

        confirm_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='confirmationSheetConfirm']"))
        )
        confirm_btn.click()

        log(f"Deleted tweet #{index + 1}")
        time.sleep(2)
    except Exception as e:
        log(f"Failed to delete tweet #{index + 1}: {type(e).__name__} - {str(e)}")

def delete_last_n_tweets():
    log("Navigating to profile...")
    go_to_profile()

    deleted = 0
    attempts = 0

    while deleted < MAX_TWEETS and attempts < 30:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
        )
        tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        if not tweets:
            log("No tweets found.")
            break

        for tweet in tweets:
            if deleted >= MAX_TWEETS:
                break
            delete_tweet(tweet, deleted)
            deleted += 1
            if deleted % SLEEP_EVERY == 0:
                log(f"Waiting {SLEEP_SECONDS} seconds after {deleted} tweets...")
                time.sleep(SLEEP_SECONDS)

        driver.refresh()
        time.sleep(4)
        attempts += 1

# ===== MAIN =====
log("Launching browser...")
login_with_cookies_or_fallback()
delete_last_n_tweets()
driver.quit()
log("Browser closed.")
