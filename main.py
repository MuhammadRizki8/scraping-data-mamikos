import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")  # To run Chrome in headless mode
driver = webdriver.Chrome(options=options)

driver.get("https://mamikos.com/cari/universitas-pendidikan-indonesia-isola-kota-bandung-jawa-barat-indonesia/all/bulanan/0-15000000?rent=2&sort=price,-&price=10000-20000000&singgahsini=0")
wait = WebDriverWait(driver, 20)

detail_urls = []  # List to store the URLs

kosts = []

try:
    for _ in range(2):
    # Click the "Load More" button
        load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "list__content-load-action")))
        load_more_button.click()

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load after scrolling
        time.sleep(5)  # Adjust the delay time as needed

    # Wait for the room list cards to be clickable
    room_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "room-list__card")))

    # Iterate through each room card in the list
    for card in room_cards:
        # Scroll into view and click each card
        driver.execute_script("arguments[0].scrollIntoView();", card)
        card.click()

        # Add a delay between clicks
        time.sleep(5)  # Delay for 1 second
        
        # Wait for new tab to open and switch to it
        wait.until(lambda driver: len(driver.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])

        # Capture the URL from the new tab
        detail_urls.append(driver.current_url)

        #===============================================================================
        wait = WebDriverWait(driver, 15)  # Wait up to 10 seconds

        # Repeat scrolling and waiting if necessary
        for _ in range(5):  # Repeat 3 times (adjust as needed)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'detail-kost-facility-item__label')))

        # Extract the page content after it's fully loaded
        html_content = driver.page_source

        # Find the title using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # title
        title_element = soup.find('p', attrs={'class':'detail-title__room-name bg-c-text bg-c-text--heading-3'})

        if title_element:
            title = title_element.text.strip()
            print(title)
        else:
            print("Title element not found.")

        # facility
        facilities = []
        facilities_elements = soup.find_all(class_="detail-kost-facility-item__label bg-c-text bg-c-text--body-2")

        # Extract the text from each element and print it
        for facility in facilities_elements:
            print(facility.get_text(strip=True))
            facilities.append(facility.get_text(strip=True))

        price_element = soup.select_one('.card-price__price > .bg-c-text.bg-c-text--body-1')

        # price
        if price_element:
            price = price_element.get_text().replace('Rp', '').replace('.', '')
            print(price)
        else:
            print("Price element not found.")

        # save

        kost = {} 
        kost['nama'] = title
        kost['fasilitas'] = '+'.join(facilities)
        kost['harga'] = price
        kosts.append(kost)

        #===============================================================================

        # Close the new tab and switch back to the main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

except TimeoutException:
    print("Failed to find or interact with room list cards.")
    driver.save_screenshot('debug_screenshot.png')

finally:
    driver.quit()

filename = 'kost.csv'
with open(filename, 'w', newline='') as f: 
    w = csv.DictWriter(f,['nama','fasilitas','harga']) 
    w.writeheader() 
    for kost in kosts:
        w.writerow(kost) 

# Print all collected URLs
print("Collected URLs:")
for url in detail_urls:
    print(url)