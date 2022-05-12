from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import pandas

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument(r"--user-data-dir=C:\Users\shubham.thakur\AppData\Local\Google\Chrome\User Data")
chromeOptions.add_argument('--profile-directory=Profile 3')
chromeOptions.add_argument("--disable-extensions")

driver = webdriver.Chrome(executable_path=r"C:\Users\shubham.thakur\Documents\chromedriver.exe", options=chromeOptions)
driver.get("https://carros.tucarro.com.co/_NoIndex_True")

max_page=int(driver.find_element_by_class_name('andes-pagination__page-count').text.split()[-1])

def get_all_elements():
     return driver.find_elements_by_xpath("//*[@class='ui-search-result__content ui-search-link']")
def get_url(var):
    return var.get_attribute('href')
def next_page():
    return driver.find_elements_by_xpath("//*[@class='andes-pagination__button andes-pagination__button--next']")[-1].click()

url_list=[]

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

url_list

df=pd.DataFrame()
df['URLS']=url_list
df.to_excel("C://Users/shubham.thakur/Downloads/URLS.xlsx")