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


# Enable cookies explicitly
profile = webdriver.FirefoxProfile()
profile.set_preference("network.cookie.cookieBehavior", 0)  # Accept all cookies by default


# Disable Firefox extensions (if necessary)
profile.set_preference("extensions.enabled", False)

# Retrieve the 2FA secret key from the .env file
two_fa_secret = os.getenv('TWO_FA_SECRET')

# Path to your geckodriver (update this to your setup)
gecko_service = Service('/usr/local/bin/geckodriver')

# Initialize the Firefox WebDriver
print("Initializing Firefox WebDriver...")
driver = webdriver.Firefox(service=gecko_service, options=options)
# Open the target website
print("Opening website...")
driver.get('https://kbs.egm.gov.tr/')

# Wait for the page to load
driver.implicitly_wait(5)

# Get all the elements available with tag name 'p'
elements = driver.find_elements(By.TAG_NAME, 'tr')

for e in elements:
    print(e.text)
  

# Step 5: Close the browser after task completion
print("Closing browser...")
driver.quit()
