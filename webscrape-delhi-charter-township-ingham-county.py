import requests
import json
import itertools
import pandas as pd
import os
import csv
import time
import sys
import urllib.request
import random
from bs4 import BeautifulSoup
from datetime import date
from htmldate import find_date
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from json import JSONDecoder
from fake_useragent import UserAgent
from solveRecaptcha import solveRecaptcha

# Henry Mangelsdorf 2022 

# driver settings
options = Options()
options.add_argument("--window-position=2000,0")
options.add_argument("--window-size=1920,1080")
options.headless = True # 12/26/2022 Now is headless because I automated the municipality click
options.add_argument("--disable-dev-shm-usage")
#options.add_argument("--no-sandbox") 
#options.add_argument("--disable-extensions")
#options.add_argument("--remote-debugging-port=9222")
#prefs = {"profile.managed_default_content_settings.images": 2}
#options.add_experimental_option("prefs", prefs)
ua = UserAgent(use_cache_server=False)
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# starting link to login page
driver.get('https://bsaonline.com/Account/LogOn?uid=269')


username = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'UserName')))
password = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'Password')))



#username.send_keys('Hmangels') #username
#password.send_keys('j.G#*U9yCvJX5_e') #!!! PASSWORD DO NOT MAKE PUBLIC !!!
#username.send_keys('Hmangels2') #username
#password.send_keys('ZBrwReMJ8:-hp8x') #!!! PASSWORD DO NOT MAKE PUBLIC !!!
username.send_keys('slegnamh') #username
password.send_keys('XCVbooT32') #!!! PASSWORD DO NOT MAKE PUBLIC !!!


# this clicks the sign in button after username and password are entered in
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[7]/div[3]/div[1]/form/div[5]/input"))).click()

time.sleep(5)

element_to_hover_over = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1)")))

hover = ActionChains(driver).move_to_element(element_to_hover_over)
hover.perform()

time.sleep(5)

WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"li[class='with-border current'] div:nth-child(3) a:nth-child(1)"))).click() # Clicks the top list item on the municipality list


# this clicks link to the Property Sale Search link where you set search parameters for the parcels you want to see
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.LINK_TEXT,"Property Sale Search"))).click()


time.sleep(random.randint(4, 6)) 

# search parameter values
saleDateRangeStart = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'SaleDateRangeFrom')))
saleDateRangeTo = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'SaleDateRangeTo')))
salePriceRangeMin = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'SalePriceFrom')))
saleDateRangeStart.clear()
saleDateRangeStart.send_keys('01/14/2022')
time.sleep(2)
saleDateRangeTo.clear()
saleDateRangeTo.send_keys('12/26/2022')
salePriceRangeMin.send_keys("125,000")
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID,"Agricultural"))).click()
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID,"TimberCutover"))).click()
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID,"Industrial"))).click()
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID,"Developmental"))).click()
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID,"Commercial"))).click()



# clicks search button after search parameters are set
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID,"search"))).click()



################################################## CAPTCHA CATCHER #################################################################
try:
    WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID,"g-recaptcha-response")))
    result = solveRecaptcha(driver.current_url)
    code = result['code']
    driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
    driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
    time.sleep(2)
    print("Captcha Solved") 
except Exception as e:
    print("No Captcha Detected")
################################################## CAPTCHA CATCHER #################################################################




# clicks drop down menu to select number of parcels to display
#WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"span[class='t-select'] span[class='t-icon t-arrow-down']"))).click()

#WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[16]/div[1]/ul[1]/li[1]"))).click() # 10 parcels displayed
#WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[16]/div[1]/ul[1]/li[6]"))).click() # 50 parcels displayed

time.sleep(20)





# clicks the >> arrow to go to the last page
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[class='t-grid-pager t-grid-top'] span[class='t-icon t-arrow-last']"))).click()



# skip pages i already did 
# i == # of csv. files already made
#for i in range(21): 
#   WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[7]/div[3]/div[1]/form[1]/div[4]/div[1]/div[1]/div[2]/a[2]/span[1]"))).click()
#   time.sleep(1)


                                                                        


csv_headers = ['Parcel/Account','City/ZIP','Address','Date Of Sale','Sale Price','Instrument','Grantor','Grantee','Term Of Sale','Year Built', 'Year, Season, SEV/Assessed_Value, PRE/MBT','Year, Season, SEV/Assessed_Value, PRE/MBT','Previous Year, Season, SEV/Assessed_Value, PRE/MBT','Previous Year, Season, SEV/Assessed_Value, PRE/MBT','Extra SEV Info']

# 0 to total pages or total pages - # of skipped pages    total for this area = (8)
total_pages = range(0,8)
for n in total_pages:
    print("Page: " + str(n))
    record_rows = []

    if n != 0: # when n == 0 it is the first page and must first be scraped before going on to the next page
        
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[7]/div[3]/div[1]/form[1]/div[4]/div[1]/div[1]/div[2]/a[2]/span[1]"))).click()
        time.sleep(2)

        ################################################## CAPTCHA CATCHER #################################################################
        try:
            WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID,"g-recaptcha-response")))
            result = solveRecaptcha(driver.current_url)
            code = result['code']
            driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
            driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
            time.sleep(2)
            print("Captcha Solved") 
        except Exception as e:
            print("No Captcha Detected")
        ################################################## CAPTCHA CATCHER #################################################################
        
    # grabs table element for table of parcels
    tbody = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(6) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(3)')))
    total_rows = len(tbody.find_elements(by=By.XPATH, value='./tr')) #  counts number of rows in parcel table                           

    time.sleep(2)
    
    for i in reversed(range(1,total_rows+1)):
        print(i)
        rows = []
        relevant_years_list = []
                                                                              
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[7]/div[3]/div[1]/form[1]/div[4]/div[1]/table[1]/tbody[1]/tr["+ str(i) +"]"))).click()

        ################################################## CAPTCHA CATCHER #################################################################
        try:
            WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID,"g-recaptcha-response")))
            result = solveRecaptcha(driver.current_url)
            code = result['code']
            driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
            driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
            time.sleep(2)
            print("Captcha Solved") 
        except Exception as e:
            print("No Captcha Detected")
        ################################################## CAPTCHA CATCHER #################################################################

        time.sleep(5)
        try:
            button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.LINK_TEXT,"Tax Information"))) # clicks tax information button to access SEV and PRE/MBT data
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)
            while True:
                try:
                    time.sleep(4)
                    element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'GetMoreYearsButton_TaxHistory')))
                    driver.execute_script("arguments[0].click();", element)
                    
                except TimeoutException as e: 
                    print(e)
                    break
                except StaleElementReferenceException as e:
                    print(e)

            html_tax_information = driver.page_source # grabs html again after tax info page has been clicked
            soup = BeautifulSoup(html_tax_information, features="lxml")
            all_sev_info = [] #list of single_sev_info

            for tag in soup.find_all(lambda tag: tag.name == 'tr' and tag.get('class') == ['container-row'] or tag.get('class') == ['container-row','g-alt'])[1:]: # everything except the 1st element which happens to be the 2022 general information on the propery info page
                try:
                    single_sev_info = [] # [year, season, SEV/ASSESSED_VALUE, PRE/MBT]
                    single_sev_info.append(tag.contents[1].text)
                    single_sev_info.append(tag.contents[2].text)
                    single_sev_info.append(tag.contents[1].find_next('tr').contents[1].contents[3].contents[1].find('th', text = 'Assessed Value').find_next('td').text)
                    single_sev_info.append(tag.contents[1].find_next('tr').contents[1].contents[3].contents[1].find('th', text = 'PRE/MBT').find_next('td').text)

                    if single_sev_info not in all_sev_info: # keeps duplicates from being added to list
                        all_sev_info.append(single_sev_info)
                except IndexError as e:
                    print(e)

            relevant_sev_info = []
            
        except TimeoutException as e:
            print(e)
            all_sev_info = [] 
            relevant_sev_info = []
            pass
        try:
            button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.LINK_TEXT,"Property Information"))) 
            driver.execute_script("arguments[0].click();", button)
        except TimeoutException as e:
            print(e)
            print('No property information tab')
            driver.execute_script("window.history.go(-1)")
            time.sleep(2)
            ################################################## CAPTCHA CATCHER #################################################################
            try:
                WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID,"g-recaptcha-response")))
                result = solveRecaptcha(driver.current_url)
                code = result['code']
                driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
                driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
                time.sleep(2)
                print("Captcha Solved") # add which line the captcha was solved on
            except Exception as e:
                print("No Captcha Detected")
            ################################################## CAPTCHA CATCHER #################################################################
            continue # skips the parcel since it has no property information page

        time.sleep(2)                                                                                    
        
        ###########################################################################################################################################
        formatCheck = False                
        try: 
            # grabs sale history table element                                                                                                
            tbodyRecords = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3)')))
        except TimeoutException as e:
            print(e)
            # below code is uncommented when there is a second page format to look out for                                                                                                
            #try:                                                                                                  
            #    tbodyRecords = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3)')))
            #    formatCheck = True
            #except TimeoutException as e: 
            #    print(e) 
            #    pass
        if formatCheck:
            print('THIS PARCEL USED SECOND FORMAT')
        
        total_rows_saleHistory = len(tbodyRecords.find_elements(by=By.XPATH, value='./tr')) # counts number of rows in table element
        html_property_information = driver.page_source #grabs html code for property information
        soup = BeautifulSoup(html_property_information, features="lxml")
        yearBuilt = soup.find('th', text = 'Year Built')
        if yearBuilt is not None:
            yearBuilt = yearBuilt = soup.find('th', text = 'Year Built').find_next('td').text
            print(yearBuilt)

        print(total_rows_saleHistory)
        # format 1
        ###########################################################################################################################################
        if not formatCheck:
            for j in range(1,total_rows_saleHistory+1):
                #collects data from each element
                parcelAccount = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[7]/div[3]/div[1]/form[1]/div[1]/div[1]/div[1]/div[3]"))).text
                time.sleep(2)
                isPresent = len(driver.find_elements(by=By.CLASS_NAME,value="sresult-header1-address")) > 0
                if isPresent:
                    cityZip = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[7]/div[3]/div[1]/form[1]/div[1]/div[1]/div[1]/div[2]/span[2]"))).text
                else:
                    cityZip = 'NA'
                
                if isPresent:
                    address = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME,"sresult-header1-address"))).text
                else:
                    address = 'NA'
                                                                                                        
                saleDate = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(1)"))).text
                                                                                                                                                                                     
                salePrice = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(2)"))).text
            
                instrument = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(3)"))).text
                
                grantor = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(4)"))).text
            
                grantee = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(5)"))).text
                
                termOfSale = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(6)"))).text
                


                relevant_year = saleDate[-4:] # makes a string of the year in this row
                relevant_years_list.append(relevant_year)

                print(address)

                if not parcelAccount:
                    parcelAccount = 'NA'
                if not cityZip:
                    cityZip = 'NA'
                if not address:
                    address = 'NA'
                if not saleDate:
                    saleDate = 'NA'
                if not salePrice:
                    salePrice = 'NA'
                if not instrument:
                    instrument = 'NA'
                if not grantor:
                    grantor = 'NA'
                if not grantee:
                    grantee = 'NA'
                if not termOfSale:
                    termOfSale = 'NA'
                if not yearBuilt:
                    yearBuilt = 'NA'

                row = [parcelAccount, cityZip, address,  saleDate, salePrice, instrument, grantor, grantee, termOfSale, yearBuilt]
                rows.append(row)
        ###########################################################################################################################################
        # format 2
        if formatCheck:
            for j in range(1,total_rows_saleHistory+1):
                #collects data from each element
                parcelAccount = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[7]/div[3]/div[1]/form[1]/div[1]/div[1]/div[1]/div[3]"))).text
                time.sleep(2)
                isPresent = len(driver.find_elements(by=By.CLASS_NAME,value="sresult-header1-address")) > 0
                if isPresent:
                    cityZip = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[7]/div[3]/div[1]/form[1]/div[1]/div[1]/div[1]/div[2]/span[2]"))).text
                else:
                    cityZip = 'NA'
                
                if isPresent:
                    address = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME,"sresult-header1-address"))).text
                else:
                    address = 'NA'                                                                         
                saleDate = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(1)"))).text
                                                                                                        
                salePrice = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(2)"))).text
            
                instrument = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(3)"))).text
                
                grantor = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(4)"))).text
            
                grantee = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(5)"))).text
                
                termOfSale = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(6)"))).text



                relevant_year = saleDate[-4:] # makes a string of the year in this row
                relevant_years_list.append(relevant_year) # relevant years are gathered in order to grab relevant tax info later

                print(address) 

                if not parcelAccount:
                    parcelAccount = 'NA'
                if not cityZip:
                    cityZip = 'NA'
                if not address:
                    address = 'NA'
                if not saleDate:
                    saleDate = 'NA'
                if not salePrice:
                    salePrice = 'NA'
                if not instrument:
                    instrument = 'NA'
                if not grantor:
                    grantor = 'NA'
                if not grantee:
                    grantee = 'NA'
                if not termOfSale:
                    termOfSale = 'NA'
                if not yearBuilt:
                    yearBuilt = 'NA'

                row = [parcelAccount, cityZip, address,  saleDate, salePrice, instrument, grantor, grantee, termOfSale, yearBuilt]
                rows.append(row)
        ########################################################################################################################################### 

        formatCheck2 = False
        try:
            # this is to grab on to the table element for extra tax info that may be on the property page                                                                                            
            tbodyRecords = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3)')))
        except TimeoutException as e:
            print(e)
            # below code is uncommented when there is a second page format to look out for                                                                                 
            #try:
            #    tbodyRecords = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3)')))
            #    formatCheck2 = True
            #except TimeoutException as e: 
            #    print(e)                                                                               
            #    pass
        total_rows_extra_sev_info = len(tbodyRecords.find_elements(by=By.XPATH, value='./tr')) # counts number of rows in the extra tax info table
        extra_info_list = []
        ###########################################################################################################################################
        # format 1
        if not formatCheck2:
            for j in range(1,total_rows_extra_sev_info+1):                                                       
                extra_year = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(1)"))).text
                extra_SEV = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(3)"))).text

                extra_info_list.append(extra_year + " : " + extra_SEV)
        ###########################################################################################################################################
        # format 2
        if formatCheck2:
            for j in range(1,total_rows_extra_sev_info+1):                                                      
                extra_year = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(1)"))).text
                extra_SEV = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(3)"))).text

                extra_info_list.append(extra_year + " : " + extra_SEV)

        extra_info_list.reverse()
        ########################################################################################################################################### 
        
        for year in relevant_years_list:
            i = 0
            j = 0
            k = 0
            l = 0
            for item in all_sev_info:
                if int(item[0]) == int(year) and item[1] == 'Winter': # filters through all the years for the sale date year's SEV (winter)
                    relevant_sev_info.append(item)
                    i += 1
            if i == 0:
                relevant_sev_info.append('NA')
                
            for item in all_sev_info:
                if int(item[0]) == int(year) and item[1] == 'Summer': # filters through all the years for the sale date year's SEV (summer)
                    relevant_sev_info.append(item)
                    j += 1
            if j == 0:
                relevant_sev_info.append('NA')
                
            for item in all_sev_info:
                if int(item[0]) == (int(year)-1) and item[1] == 'Winter': # filters through all the years for the year before's SEV (winter)
                    relevant_sev_info.append(item)
                    k += 1
            if k == 0:
                relevant_sev_info.append('NA')
                
            for item in all_sev_info:
                if int(item[0]) == (int(year)-1) and item[1] == 'Summer': # filters through all the years for the year before's SEV (summer)
                    relevant_sev_info.append(item)
                    l += 1
            if l == 0:
                relevant_sev_info.append('NA')

        print(relevant_sev_info) 
        
        i = 0
        try:
            for item in rows:
                item.append(relevant_sev_info[i])
                item.append(relevant_sev_info[i+1])
                item.append(relevant_sev_info[i+2])
                item.append(relevant_sev_info[i+3])
                i += 4
        except IndexError as e:
                print(e)

        for item in rows:
            item.append(extra_info_list)
        
        record_rows.extend(rows)
        driver.execute_script("window.history.go(-1)") # back to previous page
        ################################################## CAPTCHA CATCHER #################################################################
        try:
            WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID,"g-recaptcha-response")))
            result = solveRecaptcha(driver.current_url)
            code = result['code']
            driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
            driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
            time.sleep(2)
            print("Captcha Solved") 
        except Exception as e:
            print("No Captcha Detected")
        ################################################## CAPTCHA CATCHER #################################################################
        time.sleep(2)

    with open('delhi-charter-township-ingham-county'+str(n)+'.csv', 'w') as f:  # writes a csv. 50 parcels at a time so it is easier to start up where I left off if the program crashes
        write = csv.writer(f)
        write.writerow(csv_headers)
        write.writerows(record_rows)


time.sleep(2)

driver.close()



