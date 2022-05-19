
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import pandas as pd
results=pd.DataFrame()

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("--incognito")
chromeOptions.headless = True
chromeOptions.add_argument('--disable-gpu')
chromeOptions.add_argument("--disable-extensions")

s=Service(r'C:\Users\shubham.thakur\Documents\chromedriver.exe')
driver = webdriver.Chrome(service=s,options=chromeOptions)

def change_page(url):
    driver.get(url)
    try:
        driver.find_element(By.ID, 'newCookieDisclaimerButton').click()
    except:
        pass
def get_car_page_title():
    try:
        return driver.title
    except:
        return "Not Available"
def get_car_price():
    try:
        currency_symbol=driver.find_element(By.CLASS_NAME, "andes-money-amount__currency-symbol").text
        car_price=driver.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
        return currency_symbol+car_price
    except:
        return "Not Available"
def get_car_seller_location():
    try:
        return driver.find_element(By.ID, "seller_profile").text.split('Ubicación del vehículo\n')[1].split('\n')[0]
    except:
        return "Not Available"
def get_time_selling_in_TuCarro():
    try:
        return driver.find_element(By.ID, "seller_profile").text.split('Tiempo vendiendo en TuCarro\n')[1].split('\n')[0]
    except:
        return "Not Available"
def conditions_and_special_services():
    try:
        return driver.find_element(By.CLASS_NAME, "ui-pdp-highlighted-sale-specs").text.replace('Condiciones y servicios especiales\n',"").replace('\n'," || ")
    except:
        return "Not Available"
def get_main_features():
    try:
        features=[]
        details=[]
        for i in driver.find_elements(By.TAG_NAME,'th'):
            features.append("Main Features - "+i.text)
        for i in driver.find_elements(By.TAG_NAME,'td'):
            details.append(i.text)  
        return dict(zip(features, details))
    except:
        print('No Features')
        print(url)
def get_information_from_tabs():
    information_buttons=driver.find_elements(By.XPATH, '//div[@class="andes-tabs"]//button')
    information_tab={}
    for information_category in information_buttons:
        information_tab_details=[]
        ActionChains(driver).move_to_element(driver.find_element(By.CLASS_NAME,"ui-pdp-description__title")).perform()
        time.sleep(1)
        try:
            information_category.click()
        except:
            driver.find_element(By.CLASS_NAME,"control-arrow").click()
            information_category.click()
        for information_for_category in driver.find_elements(By.CLASS_NAME,"ui-pdp-specs__tab-spec"):
            information_tab_details.append(information_for_category.text)
        information_tab[information_category.text]=information_tab_details
    return information_tab
def get_descriptions():
    descriptions=driver.find_element(By.CLASS_NAME,"ui-pdp-description").text.split('\n')[1:]
    return descriptions
def get_all_details_in_dict_format():
    try:
        page_details_dict={}
        page_details_dict['Car Page Title']=get_car_page_title()
        page_details_dict['Car Price']=get_car_price()
        page_details_dict['Car Location']=get_car_seller_location()
        page_details_dict['Time selling in TuCarro']=get_time_selling_in_TuCarro()
        page_details_dict['Conditions and Special Services']=conditions_and_special_services()
        page_details_dict.update(get_main_features())
        page_details_dict.update(get_information_from_tabs())
        page_details_dict['Descriptions']=get_descriptions()
        page_details_dict['URL']=url
        return page_details_dict
    except:
        print('Exception Occured with info')
        print(url)


urls_data=pd.read_excel(r'C:\Users\shubham.thakur\Documents\URLS.xlsx',index_col=0)

urls_to_read=urls_data['URLS']

start = time.time()

Exceptions=[]
for url in urls_to_read[:200]:
    try:
        change_page(url)
        time.sleep(random.randint(3,10))
        results=results.append(get_all_details_in_dict_format(),ignore_index=True)
    except:
        Exceptions.append(url)        

end=time.time()

print((end-start)/60)

driver.close()

results.to_excel(r'C:\Users\shubham.thakur\Documents\tucarro_output.xlsx')
