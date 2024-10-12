import time
import pyotp
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


# Load environment variables from the .env file
load_dotenv()

options = Options()
options.binary_location = '/usr/bin/firefox-esr'  # Adjust this path if needed
options.add_argument('--headless')  # This enables headless mode

# Retrieve the 2FA secret key from the .env file
two_fa_secret = os.getenv('TWO_FA_SECRET')

# Path to your geckodriver (update this to your setup)
gecko_service = Service('/usr/local/bin/geckodriver')

# Initialize the Firefox WebDriver
print("Initializing Firefox WebDriver...")
driver = webdriver.Firefox(service=gecko_service, options=options)
# Open the target website
print("Opening website...")
driver.get('https://kbs.egm.gov.tr/my.policy')

# Wait for the page to load
driver.implicitly_wait(5)

# Step 1: Fill in the login details
print("Filling in login details...")

# Fill the Username (input_1)
username_field = driver.find_element(By.CSS_SELECTOR, "#input_1")
username_field.send_keys('semihyayli@hotmail.com')
print("Username entered.")


# Fill the TC Kimlik No (input_2)
id_number_field = driver.find_element(By.CSS_SELECTOR, '#input_2')
id_number_field.send_keys('41848910588')
print("TC Kimlik No entered.")

# Fill the Password (input_3)
password_field = driver.find_element(By.CSS_SELECTOR, '#input_3')
password_field.send_keys('905549')
print("Password entered.")

# Submit the login form
submit_button = driver.find_element(By.CSS_SELECTOR, '.credentials_input_submit')
submit_button.click()
print("Login form submitted.")

# Wait for the new page to load (the 2FA page)
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '#input_1'))
)
print("2FA page loaded.")

# Step 2: Generate the 2FA token using the secret key from .env
totp = pyotp.TOTP(two_fa_secret)  # Loaded from .env
two_fa_code = totp.now()

print(f"Generated 2FA Code: {two_fa_code}")

# Step 3: Fill in the 2FA token
two_fa_input = driver.find_element(By.ID, '.input_1')  # Assuming the token field is input_1
two_fa_input.send_keys(two_fa_code)
print("2FA code entered.")

# Step 4: Submit the 2FA form
submit_button = driver.find_element(By.CSS_SELECTOR, '.credentials_input_submit')
submit_button.click()
print("2FA form submitted.")

# Optionally, wait or capture the response after submission
time.sleep(5)
print("Waiting for post-login actions to complete...")

# Step 5: Close the browser after task completion
print("Closing browser...")
driver.quit()
