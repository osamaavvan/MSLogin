import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

if len(sys.argv) != 2:
    print("Usage: python3 app.py <emails.txt>")
    sys.exit(1)

email_file = sys.argv[1]

try:
    with open(email_file, 'r') as f:
        email_list = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Error: File '{email_file}' not found.")
    sys.exit(1)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

valid_emails = []

for email in email_list:
    try:
        driver.get("https://login.microsoftonline.com/")
        time.sleep(3)

        # Enter email
        email_input = driver.find_element(By.NAME, "loginfmt")
        email_input.clear()
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)

        time.sleep(3)

        try:
            error_msg = driver.find_element(By.ID, "usernameError")
            if "incorrect" in error_msg.text:
                print(f"[✗] Invalid email: {email}")
                continue
        except NoSuchElementException:
            print(f"[✓] Valid email: {email}")
            valid_emails.append(email)

        driver.execute_script("window.history.go(-1)")
        time.sleep(2)

    except Exception as e:
        print(f"Error checking {email}: {e}")
        continue

with open('valid_emails.txt', 'w') as f:
    for email in valid_emails:
        f.write(email + '\n')

driver.quit()
print("Done.")
