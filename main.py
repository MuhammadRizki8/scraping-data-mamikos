from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = Options()
options.headless = False  # Disable headless mode to visually debug
driver = webdriver.Chrome(options=options)

driver.get("https://mamikos.com/cari/universitas-pendidikan-indonesia-isola-kota-bandung-jawa-barat-indonesia/all/bulanan/0-15000000?rent=2&sort=price,-&price=10000-20000000&singgahsini=0")
wait = WebDriverWait(driver, 20)

detail_urls = []  # List to store the URLs

try:
    # Wait for the room list cards to be clickable
    room_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "room-list__card")))

    # Iterate through each room card in the list
    for card in room_cards:
        # Scroll into view and click each card
        driver.execute_script("arguments[0].scrollIntoView();", card)
        card.click()
        
        # Wait for new tab to open and switch to it
        wait.until(lambda driver: len(driver.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])

        # Capture the URL from the new tab
        detail_urls.append(driver.current_url)

        # Close the new tab and switch back to the main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

except TimeoutException:
    print("Failed to find or interact with room list cards.")
    driver.save_screenshot('debug_screenshot.png')

finally:
    driver.quit()

# Print all collected URLs
print("Collected URLs:")
for url in detail_urls:
    print(url)
