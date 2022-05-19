from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import pandas as pd

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("--incognito")
chromeOptions.headless = True
chromeOptions.add_argument('--disable-gpu')
chromeOptions.add_argument("--disable-extensions")

s=Service(r'C:\Users\shubham.thakur\Documents\chromedriver.exe')
driver = webdriver.Chrome(service=s,options=chromeOptions)

driver.get("https://carros.mercadolibre.com.co/_NoIndex_True")
time.sleep(5)
try:
    driver.find_element(By.XPATH,'//*[ contains (text(), "Entendido" ) ]').click()
except:
    pass
try:
    driver.find_element(By.XPATH,'//button[@class="andes-tooltip-button-close"]').click()
except:
    pass


max_page=int(driver.find_element(By.CLASS_NAME,'andes-pagination__page-count').text.split()[-1])


def get_all_elements():
     return driver.find_elements(By.XPATH,"//*[@class='ui-search-result__content ui-search-link']")
def get_url(var):
    return var.get_attribute('href')
def next_page():
    action = ActionChains(driver)
    tab_next_page=driver.find_elements(By.XPATH,"//*[@class='andes-pagination__button andes-pagination__button--next']")[-1]
    return action.move_to_element_with_offset(tab_next_page, 10, 20).click().perform()


url_list=[]

start=time.time()

for i in range(0,max_page):
    print(i)
    time.sleep(random.randint(1,5))
    elements=get_all_elements()
    for elem in elements:
        url_list.append(get_url(elem))
    time.sleep(random.randint(1,10))
    try:
        next_page()
    except:
        break

end=time.time()

print(end-start)

driver.close()

df=pd.DataFrame()
df['URLS']=url_list
df.to_excel("C://Users/shubham.thakur/Documents/Carros_URLS.xlsx")