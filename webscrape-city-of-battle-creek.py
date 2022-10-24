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
from json import JSONDecoder
from fake_useragent import UserAgent
from solveRecaptcha import solveRecaptcha


# Henry Mangelsdorf 2022 

# driver settings
options = Options()
options.add_argument("--window-position=2000,0")
options.add_argument("--window-size=1920,1080")
#chrome_options.headless = True 
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


#starting link to login page
driver.get('')
driver.implicitly_wait(0)

username = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'UserName')))
password = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'Password')))

username.send_keys('') # username
password.send_keys('') #!!! PASSWORD DO NOT MAKE PUBLIC !!!


# this clicks the sign in button after username and password are entered in
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[7]/div[3]/div[1]/form/div[5]/input"))).click()

time.sleep(20)

address_list = []

# this takes in the address list that has been collected from zillow or a different county with a property search
with open('calhoun-county-battle-creek-address-list.csv') as csv_address: 
        csv_reader = csv.reader(csv_address, delimiter='\n')
        for row in csv_reader:
            address_list.append(row[0])
csv_address.close



adress_list_row_count = len(address_list)
print("Total Addresses : " + str(adress_list_row_count))

for n in range(0,adress_list_row_count+1):
    record_rows = []
    time.sleep(random.randint(4, 10)) 
    searchText = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'SearchText')))

    print("Searching:" + address_list[n] + " n = " + str(n))

    searchText.clear()
    # enters the address from the address list
    searchText.send_keys(address_list[n])
    time.sleep(random.randint(4, 10)) 

    # clicks the search button
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[value='Search']"))).click()
    time.sleep(10)

    ################################################## CAPTCHA CATCHER #################################################################
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"g-recaptcha-response")))
        
        result = solveRecaptcha(driver.current_url)
        code = result['code']
        driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
        driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
        time.sleep(2)
        print("Captcha Solved") 
    except Exception as e:
        pass
    ################################################## CAPTCHA CATCHER #################################################################
    
    time.sleep(random.randint(4,10))

    
    zero_rows = ""
    
    # this is to detect if no results are returned from the search
    try:
        zero_rows = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"td[colspan='4']"))).text
    except TimeoutException as e:
        print(e)
        try:
            zero_rows = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"td[colspan='4']"))).text
        except TimeoutException as e:
            print(e)
    
    time.sleep(random.randint(4, 10)) 
    
    if zero_rows == "No records to display.":
        print("Skipping because no results " + address_list[n])
        continue    
    try:    
        tbody = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'/html[1]/body[1]/div[7]/div[3]/div[1]/form[1]/div[4]/div[1]/table[1]/tbody[1]')))
    except TimeoutException as e:                                                     
        print(e)

   
    total_rows = len(tbody.find_elements(by=By.XPATH, value='./tr'))
    print('Number of Rows ' + str(total_rows))  

    # alternative way of checking if no results are returned
    #if total_rows == 0:
    #    print("Skipping because no results " + address_list[n])
    #    continue   

    if total_rows > 1: # i skip these for now and will come back later
        with open('skipped-adresses-marshall-twp.csv', mode='a') as skipped_addresses:
            writer = csv.writer(skipped_addresses, delimiter='\n')
            writer.writerow([address_list[n]])
        skipped_addresses.close()
        print("Skipping because more than one result " + address_list[n])
        continue                



    
    for i in reversed(range(1,total_rows+1)):
        print(address_list[n] + " i = " + str(i))
        rows = []
        relevant_years_list = []
        # this clicks on the parcel link                                                                       
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[7]/div[3]/div[1]/form[1]/div[4]/div[1]/table[1]/tbody[1]/tr["+ str(i) +"]"))).click()

        ################################################## CAPTCHA CATCHER #################################################################
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"g-recaptcha-response")))
            
            result = solveRecaptcha(driver.current_url)
            code = result['code']
            driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
            driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
            time.sleep(2)
            print("Captcha Solved")
        except Exception as e:
            pass
        ################################################## CAPTCHA CATCHER #################################################################

        time.sleep(5)
        try:
            button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.LINK_TEXT,"Tax Information"))) # click tax information button to access SEV and PRE/MBT data
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)
            while True:
                try:
                    time.sleep(5)
                    element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'GetMoreYearsButton_TaxHistory')))
                    driver.execute_script("arguments[0].click();", element)
                    
                except TimeoutException as e:
                    print(e)
                    break
                except StaleElementReferenceException as e:
                    print(e)

            html_tax_information = driver.page_source # grabs html again after tax info page has been clicked
            soup = BeautifulSoup(html_tax_information, features="lxml")
            all_sev_info = [] # list of single_sev_info

            for tag in soup.find_all(lambda tag: tag.name == 'tr' and tag.get('class') == ['container-row'] or tag.get('class') == ['container-row','g-alt'])[1:]: # Everything except the 1st element which happens to be the 2022 general information on the propery info page
                try:
                    single_sev_info = [] # format = [year, season, SEV/ASSESSED_VALUE, PRE/MBT]
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
            continue # skips the parcel if it has no property information page
        time.sleep(4)
                                                                                                            
        # counts number of Sales Records being displayed
        formatCheck = False 
        sale_history_check = False 
        try:              
            tbodyRecords = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3)')))
        except TimeoutException as e:
            print(e) 
            # this is if for when there is a second parcel page format                                                                                               
            #try:
                #tbodyRecords = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3)')))
                #formatCheck = True
            #except TimeoutException as e: 
                #print(e) 
                #pass

        
        total_rows_saleHistory = len(tbodyRecords.find_elements(by=By.XPATH, value='./tr'))
        html_property_information = driver.page_source # grabs html code for propety information
        soup = BeautifulSoup(html_property_information, features="lxml")
        yearBuilt = soup.find('th', text = 'Year Built')

        if yearBuilt is not None:
            yearBuilt = yearBuilt = soup.find('th', text = 'Year Built').find_next('td').text
            print(yearBuilt)
        print(total_rows_saleHistory)

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
                                                                                                                                                                                        
                try:
                    salePrice = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(2)"))).text
                except TimeoutException as e: 
                    print(e) 
                    print("No Sale History Found")
                    sale_history_check = True
                    continue # this breaks the loop so the parcel can be skipped when there is no sale history
                instrument = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(3)"))).text
                
                grantor = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(4)"))).text
            
                grantee = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(5)"))).text
                
                termOfSale = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(6)"))).text
                


                relevant_year = saleDate[-4:] # makes a string of the year in this row
                relevant_years_list.append(relevant_year)

                print(address) # to see progress

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
        if sale_history_check: # if there is no sale history the parcel is skipped
            continue
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
                try:                                                                                     
                    salePrice = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(2)"))).text
                except TimeoutException as e: 
                    print(e) 
                    print("No Sale History Found")
                    sale_history_check = True
                    continue
                instrument = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(3)"))).text
                
                grantor = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(4)"))).text
            
                grantee = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(5)"))).text
                
                termOfSale = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(6)"))).text



                relevant_year = saleDate[-4:] # makes a string of the year in this row
                relevant_years_list.append(relevant_year)

                print(address) # to see progress

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
        if sale_history_check:
            continue
        formatCheck2 = False
        try:                                                                                                   
            tbodyRecords = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3)')))
        except TimeoutException as e:
            print(e) 
            # this is for when there is a second parcel page format                                                                                
            #try:                                                                                                    
                #tbodyRecords = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(7) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3)')))
                #formatCheck2 = True
            #except TimeoutException as e: 
                #print(e)                                                                               
                #pass
        total_rows_extra_sev_info = len(tbodyRecords.find_elements(by=By.XPATH, value='./tr'))
        extra_info_list = []

        if not formatCheck2:
            for j in range(1,total_rows_extra_sev_info+1):                                                       
                extra_year = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(1)"))).text
                extra_SEV = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(8) > div:nth-child(5) > div:nth-child(1) > form:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(10) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child("+ str(j) +") > td:nth-child(3)"))).text

                extra_info_list.append(extra_year + " : " + extra_SEV)
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
                if int(item[0]) == int(year) and item[1] == 'Winter': # filters through all the years for the sale date year and the year before
                    relevant_sev_info.append(item)
                    i += 1
            if i == 0:
                relevant_sev_info.append('NA')
                
            for item in all_sev_info:
                if int(item[0]) == int(year) and item[1] == 'Summer': # filters through all the years for the sale date year and the year before
                    relevant_sev_info.append(item)
                    j += 1
            if j == 0:
                relevant_sev_info.append('NA')
                
            for item in all_sev_info:
                if int(item[0]) == (int(year)-1) and item[1] == 'Winter': # filters through all the years for the sale date year and the year before
                    relevant_sev_info.append(item)
                    k += 1
            if k == 0:
                relevant_sev_info.append('NA')
                
            for item in all_sev_info:
                if int(item[0]) == (int(year)-1) and item[1] == 'Summer': # filters through all the years for the sale date year and the year before
                    relevant_sev_info.append(item)
                    l += 1
            if l == 0:
                relevant_sev_info.append('NA')

        print(relevant_sev_info) # for testing
        
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

        ########################################################################################################################################### 

        for item in rows:
            item.append(extra_info_list)
        
        ########################################################################################################################################### 
        
        record_rows.extend(rows)
        driver.execute_script("window.history.go(-1)") # back to previous page
        
        time.sleep(2)
        ################################################## CAPTCHA CATCHER #################################################################
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"g-recaptcha-response")))
            
            result = solveRecaptcha(driver.current_url)
            code = result['code']
            driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
            driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
            time.sleep(2)
            print("Captcha Solved")
        except Exception as e:
            pass
        ################################################## CAPTCHA CATCHER #################################################################

    csv_parcel = open('city-of-battle-creek-11_20_2018-10_20_2022.csv', 'a') 
    writer = csv.writer(csv_parcel)
    writer.writerows(record_rows)
    csv_parcel.close()

    

        

    


time.sleep(2)

driver.close()



