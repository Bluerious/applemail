"""
Beware, this code uses Polish names for some buttons.
If needed, change the website language to Polish or change the code manually.
If you're running the code for the first time - you need to run login_and_save_cookies() function
It saves your cookies to a text file, and then you can just run create_alias() until it stops working.
"""

from selenium import webdriver
import time
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

COOKIES_FILE = "icloud_cookies.json"


# Now we'll be defining some functions that will help us save your cookie file.
def save_cookies(driver, filename):
    with open(filename, 'w') as file:
        json.dump(driver.get_cookies(), file)


def load_cookies(driver, filename):
    with open(filename, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)


def login_and_save_cookies():
    driver = webdriver.Chrome()
    driver.get("https://www.icloud.com/")

    print("Log in manually (using 2FA). Then, without closing the tab, click 'ENTER'' here.")
    input(">>>")

    save_cookies(driver, COOKIES_FILE)
    driver.quit()


# This function is optional, it will help us keep count of the email we're creating.
# For example, you're creating email nr 420 then its alias will be 420
def read_and_increment_email_count(file_path):
    try:
        # Reading the number from text file
        with open(file_path, 'r') as file:
            email_count = int(file.read().strip())
    except FileNotFoundError:
        # If the file doesn't exist, start with number 0
        email_count = 0
    except ValueError:
        # If the file is corrupted, set to 0
        email_count = 0

    # Adding 1 to the count
    new_email_count = email_count + 1

    # Replacing old number with the new one
    with open(file_path, 'w') as file:
        file.write(str(new_email_count))

    return new_email_count


# This is going to be our main function.
def create_alias():
    driver = webdriver.Chrome()
    driver.get("https://www.icloud.com/")
    time.sleep(2)

    # With open icloud website, we load the cookies
    if os.path.exists(COOKIES_FILE):
        load_cookies(driver, COOKIES_FILE)
        driver.refresh()
        time.sleep(2)
    else:
        print("No cookies saved. Please check the issue and run login_and_save_cookies().")
        driver.quit()  # This condition could be automated, but it may affect the customer
        return

    # Go to tab where new hidden emails are created
    driver.get("https://www.icloud.com/icloudplus/")
    time.sleep(2)

    wait = WebDriverWait(driver, 20)
    try:
        # First, we click the "Hide my email button"
        hide_my_email_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Ukryj mój adres email')]"))
        )  # This here -> change to your language
        hide_my_email_button.click()
        time.sleep(3)

        # We've just entered an iframe on the website. Need to do so in the code too.
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        how_many_now_emails = 5
        # For now, you can create 5 new emails per hour, so we run the generating code 5 times
        for _ in range(how_many_now_emails):
            # Now we need to click the "+"
            plus_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@title='Dodaj']"))
            )
            plus_button.click()
            time.sleep(3)

            # Find text box corresponding to alias
            alias_input = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "form-textbox-input"))
            )
            time.sleep(3)
            # Now we need to write our alias.
            # We could write something random
            # This code uses our defined functions to keep count of the emails
            file_path = "email_count.txt"
            new_email_number = read_and_increment_email_count(file_path)
            print(f"New e-mail number: {new_email_number}")
            alias_input.send_keys(str(new_email_number))
            time.sleep(3)

            # Click the button to create the email
            create_email_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Utwórz adres email')]"))
            )
            create_email_button.click()
            time.sleep(3)

            # Click the button to go back
            go_back_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Wstecz')]"))
            )
            go_back_button.click()
            time.sleep(3)

    except Exception as e:
        print("Error:", e)

    driver.quit()


# --- First run (and possibly later, when cookies change) ---
# login_and_save_cookies()

# --- Every other run ---
# create_alias()

# --- Or if you want automation ---
while True:
    create_alias()
    time.sleep(3600)
