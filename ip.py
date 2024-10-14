from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver for Safari
driver = webdriver.Safari()

# Open the website (assuming Flipkart)
driver.get('https://www.flipkart.com/apple-iphone-13-starlight-128-gb/p/itmc9604f122ae7f?pid=MOBG6VF5ADKHKXFX&lid=LSTMOBG6VF5ADKHKXFXZVXGTL&marketplace=FLIPKART&q=iphone13&store=tyy%2F4io&srno=s_1_3&otracker=AS_Query_OrganicAutoSuggest_5_7_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_5_7_na_na_na&fm=organic&iid=58bba978-55bd-4b6f-ab5d-4b328b10e3ed.MOBG6VF5ADKHKXFX.SEARCH&ppt=pp&ppn=pp&ssid=4brfme0ulc0000001727025645824&qH=7d4afaedfc628b80')

# Wait for the page to load
time.sleep(3)

try:
    # Close any popup or initial screen if there is one (specific to Flipkart)
    close_popup_button = driver.find_element(By.CSS_SELECTOR, 'button._2KpZ6l._2doB4z')
    close_popup_button.click()
    time.sleep(1)
except:
    pass  # If no popup exists, continue

# Locate the "Login" button (use a CSS selector or an XPath based on the actual webpage structure)
login_button = driver.find_element(By.CSS_SELECTOR, 'a._1_3w1N')  # Adjust the selector as per the page
login_button.click()

# Wait for the login modal to appear
time.sleep(2)

# Enter the phone number in the input field
phone_input = driver.find_element(By.CSS_SELECTOR, 'input._2IX_2-.VJZDxU')  # Adjust selector as needed
phone_input.send_keys('8595715949')  # Input the phone number

# Click the "Request OTP" button (or "Login" button)
request_otp_button = driver.find_element(By.CSS_SELECTOR, 'button._2KpZ6l._2HKlqd._3AWRsL')  # Adjust the selector
request_otp_button.click()

# Wait for manual OTP input if automation isn't set up for that (you may need to input OTP manually)
time.sleep(10)  # Adjust time based on how long OTP takes to arrive

# Optionally, locate the OTP input field and automate OTP input (if you have an automated way to retrieve the OTP)
# otp_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter OTP"]')
# otp_input.send_keys('YOUR_OTP')  # Replace with the actual OTP received

# Finalize the login process (button after OTP input)
# confirm_button = driver.find_element(By.CSS_SELECTOR, 'button.submit-button')  # Adjust selector as needed
# confirm_button.click()

# Print success or handle exceptions
print("Login process initiated successfully!")

# Wait for a few seconds to ensure actions are complete
time.sleep(5)

# Close the browser
driver.quit()
