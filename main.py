import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Set the path to chromedriver
service = Service(executable_path='chromedriver.exe')


query = input('What do you want to search? ')


browser = webdriver.Chrome(service=service)
browser.get('https://www.google.com')

# Accept cookies if necessary (optional, depending on location/language)
try:
    WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button/div[contains(text(), "Accept all")]'))
    ).click()
except:
    pass

# Wait until the search box is interactable
search_box = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.NAME, 'q'))
)

search_box.clear()
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)

# Wait for the results
WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.yuRUbf a'))
)


results = browser.find_elements(By.CSS_SELECTOR, 'div.yuRUbf a')
links = [result.get_attribute('href') for result in results[:4]]
browser.quit()

# Create main directory
root_folder = 'scraped_links'
os.makedirs(root_folder, exist_ok=True)


for idx, link in enumerate(links):
    browser = webdriver.Chrome(service=service)
    browser.get(link)

    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'p'))
        )
        paragraphs = browser.find_elements(By.TAG_NAME, 'p')
        paragraph_texts = [p.text for p in paragraphs if p.text.strip()]
    except:
        paragraph_texts = []

    browser.quit()

    # Create the folder and save the paragraphs
    folder_name = f'link_{idx+1}'
    full_path = os.path.join(root_folder, folder_name)
    os.makedirs(full_path, exist_ok=True)

    file_path = os.path.join(full_path, 'info.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'Link: {link}\n')
        f.write('Extracted paragraphs:\n')
        for paragraph in paragraph_texts:
            f.write(paragraph + '\n')

    print(f'Saved info to {file_path}')
