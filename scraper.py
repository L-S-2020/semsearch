import chromadb, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

client = chromadb.HttpClient()
collection_search = client.get_or_create_collection(name="search")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

waitlist = ['https://wikipedia.org']
scraped = []
connect = {}
number = 0
while waitlist != []:
    current = waitlist.pop(0)
    if current not in scraped:
        try:
            driver.get(current)
            time.sleep(3)
        except:
            continue
        text = driver.find_element(By.XPATH, "/html/body").text
        for link in driver.find_elements(By.XPATH, "//a[@href]"):
            l = link.get_attribute('href')
            if l not in scraped:
                waitlist.append(l)
        try:
            title = driver.title
            print(title)
        except:
            title = str(current)
        content = []
        metadata = []
        ids = []
        content.append(text)
        metadata.append({"url": current, "name": title})
        ids.append(str(number))
        collection_search.add(
            documents=content,
            metadatas=metadata,
            ids=ids,
        )
        scraped.append(current)
        print('Scraped ' + str(current))
        number += 1
driver.quit()