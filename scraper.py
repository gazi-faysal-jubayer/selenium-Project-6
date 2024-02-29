from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pandas as pd
import time
import os
import math

columns = [
    'Company Name', 'Country', 'State', 'City', 'Street Address', 'Website', 'Phone', 'Email'
]
output_file = 'output.csv' #output file name and directory

# Check if the output file already exists
if not os.path.isfile(output_file):
    empty_df = pd.DataFrame(columns=columns)
    empty_df.to_csv(output_file, index=False)

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()
mainlink = 'https://www.fidi.org/find-fidi-affiliate?company=&off-u67qakwebod=All+companies&country=All&off-32tpsz3u6hc=All+countries&speciality%5B35%5D=35'
driver.get(mainlink)


while True:
    # Wait for an element to be present on the page before continuing
    wait = WebDriverWait(driver, 10)
    # Replace 'YOUR_SELECTOR' with the appropriate selector for the element you want to wait for
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fafapage-content__column.fafapage-content__column--results.js-accordion-processed')))

    country_block = driver.find_elements(By.CLASS_NAME, "fafa-grouping")
    for i in range(len(country_block)):
        country = country_block[i].find_element(By.CLASS_NAME, "fafa-grouping-header__title").text
        # print(country)
        state_block = country_block[i].find_elements(By.CLASS_NAME, 'fafa-city-block')
        for j in range(len(state_block)):
            state = state_block[j].find_element(By.CLASS_NAME, "fafa-city-block__title").text
            # print(state)
            block = state_block[j].find_elements(By.CLASS_NAME, 'fafa-city-block__item')
            for k in range(len(block)):
                try:
                    company_name = block[k].find_element(By.CLASS_NAME, "affiliate-teaser__title").text
                except NoSuchElementException:
                    company_name = "N/A"
                try:
                    company_link = block[k].find_element(By.CLASS_NAME, "affiliate-teaser__site-container").text
                except NoSuchElementException:
                    company_link = "N/A"
                try:
                    add = block[k].find_elements(By.CLASS_NAME, "affiliate-teaser__address-block-line")
                    city = add[1].text
                    street_address = add[0].text
                except NoSuchElementException:
                    city = "N/A"
                    street_address = "N/A"
                try:
                    ph = block[k].find_element(By.CLASS_NAME, "field--name-field-af-telephone-number field--type-telephone").text
                    phone = f'({ph})'
                except NoSuchElementException:
                    phone = "N/A"
                try:
                    email = block[k].find_element(By.CLASS_NAME, "field--name-field-af-email-address field--type-email").text
                except NoSuchElementException:
                    email = "N/A"
                
                data = {
                    'Country': country,
                    'State': state,
                    'City': city,
                    'Street Address': street_address,
                    'Company Name': company_name,
                    'Website': company_link,
                    'Phone': phone,
                    'Email': email
                }
                data_list = [data]
                existing_data = pd.read_csv(output_file) 
                new_data_df = pd.DataFrame(data_list, columns=columns)
                updated_data = existing_data._append(new_data_df, ignore_index=True)
                updated_data.to_csv(output_file, index=False)
                time.sleep(1)
    try:            
        next_page = "li[class='pager__item pager__item--next'] a span"

        # # Check if the next page element exists
        next_page_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, next_page)))

        driver.execute_script("arguments[0].click();", next_page_element)
    except (TimeoutException, StaleElementReferenceException) as e:
        # print(f"Exception: {e}")
        # print(f"Next page element not found. Exiting the loop.")
        break
        