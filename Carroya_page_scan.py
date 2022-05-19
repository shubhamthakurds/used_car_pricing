from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pandas as pd

# webdriver initializations
def get_chrome_driver():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.headless = True
    chromeOptions.add_argument('--disable-gpu')
    s=Service(r'C:\Users\shubham.thakur\Documents\chromedriver.exe')
    driver = webdriver.Chrome(service=s,options=chromeOptions)
    return driver

def change_page(url):
    try:
        driver.get(url)
    except:
        time.sleep(5)
        driver.get(url)        
    try:
        driver.find_element(By.ID, 'consent_prompt_submit').click()
    except:
        pass
    time.sleep(random.randint(2,7))
    return driver

get_chrome_driver()
driver = get_chrome_driver()
output=pd.DataFrame()
urls=pd.read_excel(r'C:\Users\shubham.thakur\Downloads\car_urls.xlsx',index_col=0)['URL']

def scrap_brand():
    try:
        brand_info = driver.find_element(By.ID, value="brandAndLineInfo").text.replace('\n',' ')
        return {'Brand Info':brand_info}
    except:
        return ''

def scrap_price():
    try:
        price_info = driver.find_element(By.XPATH, value="//*[@class='contentPrice']")
        return {'Car Price': price_info.text.split()[0]}
    except:
        return ''

def scrap_usage_km_year():
    try:
        km = driver.find_element(By.XPATH, value="//*[@class='h3P kilometers']").text
        year=driver.find_element(By.XPATH, value="//*[@class='h3P year']").text
        return {'KM':km,'Year':year}
    except:
        return ''

def scrap_seller_comment():
    try:
        seller_comment_info = driver.find_element(by=By.ID,value="sellerComments")
        seller_comment = seller_comment_info.text.split('\n')
        comment = ''
        for comm in range(1,len(seller_comment)):
            comment+= seller_comment[comm]
        return {'Seller Comment':comment}
    except:
        return ''

def scrap_features():
    try:
        feature_info = driver.find_elements(by=By.XPATH,value="//*[@class='flexContainer information']")
        feature_info_dict={}
        for i in feature_info:
            feature_=i.find_element(By.TAG_NAME,'h5').text
            info_=i.find_element(By.TAG_NAME,'h4').text
            feature_info_dict[feature_]=info_ 
        try:
            del feature_info_dict['PLACA']
        except:
            pass
        return feature_info_dict
    except:
        return ''
def get_dropdown_features():
    try:
        feature_details_dict={}
        feature_dropdown_elements=driver.find_elements(By.CLASS_NAME,'ant-collapse-item')[1:-1]
        for feature_dropdown_element in feature_dropdown_elements:
            try:
                feature_name=feature_dropdown_element.find_element(By.CLASS_NAME,'ant-collapse-header').text
                feature_details=[]
                feature_detail_elements=feature_dropdown_element.find_elements(By.CLASS_NAME,'name')
                for feature_detail in feature_detail_elements:
                    feature_details.append(feature_detail.get_attribute('innerHTML'))
                feature_details_dict[feature_name]=feature_details
            except:
                continue
        return feature_details_dict
    except:
        return ''      


def get_info_from_page():
    page_details={}
    page_details.update(scrap_brand())
    page_details.update(scrap_price())
    page_details.update(scrap_usage_km_year())
    page_details.update(scrap_seller_comment())
    page_details.update(scrap_features())
    page_details.update(get_dropdown_features())
    page_details.update({'URL':url})
    return page_details

for url in urls[0:200]:
    change_page(url)
    try:
        output=output.append(get_info_from_page(),ignore_index=True)
    except:
        time.sleep(5)
        output=output.append(get_info_from_page(),ignore_index=True)


driver.close()

output.to_csv(r'C:\Users\shubham.thakur\Documents\Carroya_page_scan_data.csv')