#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:48:19 2017

@author: katerinadoyle
@author: Guy Simons
"""

import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import os

###########################GLOBAL VARIABLES & OPTIONS##############################
os.chdir('/Users/katerinadoyle/Dropbox/repos/future_bus_school')
#dat = pd.read_csv("company_indeed.csv", sep=",", header = None, index_col=None)
#dat = pd.read_csv("comp_need_reviews.csv", sep=",", index_col=None, header=None)
dat = pd.read_csv("norway_emp_names.csv", sep=",", index_col = None)
#companies = ["Accenture", "RSPCA"]
#companies = dat.iloc[:,1] #still contains duplicate entries for companies nominated as best in several countries
#companies = companies.unique()
#countries = ["United States", "Netherlands", "United Kingdom", "Australia", "Ireland"]

companies = dat.iloc[:,0]

homepage = "https://www.indeed.com/Best-Places-to-Work"
chromedriver_path = "/Users/guysimons/Documents/BISS/FuturizingBusinessSchools/Scraping Python/Drivers/chromedriver"
firefoxdriver_path = '/Users/katerinadoyle/Documents/java/webscraping/drivers/geckodriver'

###########################DEFINE HELPER FUNCTIONS##############################
def init_driver():
    driver = webdriver.Firefox(executable_path=firefoxdriver_path) #changed this. Chrome takes too much CPU on my mac
    driver.wait = WebDriverWait(driver, 5)
    driver.implicitly_wait(5)
    return driver
    
def navigate_to_company_page(driver, company_name, homepage):
     driver.get(homepage)
     time.sleep(1)
     inputElement = driver.find_element_by_name('q')
     inputElement.clear()
     inputElement.send_keys(company_name)
     time.sleep(1)
     driver.find_element_by_id("cmp-discovery-cs-submit").click()
     time.sleep(1)
     company_found = driver.find_element_by_xpath("//div[@class = 'cmp-company-tile-blue-name']")       
     match = re.search(company_name, company_found.text)
     if match:
         rev_btn = driver.find_element_by_xpath("//div[@class='cmp-tile-footer-element']/a[@data-tn-element='reviews-footer-link']")
         rev_btn.click()
         time.sleep(2)
         select = Select(driver.find_element_by_id("cmp-loc-select"))
         select.select_by_visible_text("(all)")
         time.sleep(1)

def get_content(driver):
     txt_rev = driver.find_elements_by_xpath("//span[@class='cmp-review-text']")
     pros = driver.find_elements_by_xpath("//div[@class='cmp-review-pro-text']")
     cons = driver.find_elements_by_xpath("//div[@class='cmp-review-con-text']")
     return txt_rev, pros, cons
     
def next_page(driver):
     nxt_button = driver.find_element_by_xpath("//a[@data-tn-element='next-page']")
     time.sleep(3)
     nxt_button.click()
     time.sleep(3)

#def no_company(driver):
#    text = "We don't have much information about"
#    no_comp = driver.find_elements_by_xpath("//div[@id='cmp-zrp-container']/div[contains(text(), text)]")
#    if no_comp[0].text == "We don't have much information about " + company + ".":
#        break
#    else:
#        next_page(driver)        
    
###########################COLLECT COMPANY LIST##############################  



###########################EXECUTION##############################  
driver = init_driver()

#for country in range(0, len(countries)):
    
    # script ended at accenture revies 3640 with stale element reference
    # DO ACCENTURE AT THE END. 10000 reviews...

no_reviews_found = []
for company in range(16, len(companies)):
     print ("looking for " + companies[company])
#for company in range(0, 3):
     try:
         navigate_to_company_page(driver, companies[company], homepage)
         print("reviews found for "+ companies[company])
         review_text = []
         pros_text = []
         cons_text = []
         while True:
              print ("next page")
              text_review, pros, cons = get_content(driver)
              for i in text_review:
                   review_text.append(i.text)
              for i in pros:
                   pros_text.append(i.text)
              for i in cons:
                   cons_text.append(i.text)
    
              try:
                   next_page(driver)
              except:
                   break
     except NoSuchElementException:
         print ("no reviews for " + companies[company])
         no_reviews_found.append(companies[company])
         continue
     
     #writing content to csv files. Normally a helper function is called for this, but for some reason this results in wrong results here.
     company_names_reviews = [companies[company]] * len(review_text)
     content_dataframe_reviews = pd.DataFrame({'company_name':company_names_reviews, 'content':review_text})
     content_dataframe_reviews.to_csv("review_norway.csv", sep=';', mode = 'a', header = False, index=False)
     
     company_names_pros = [companies[company]] * len(pros_text)
     content_dataframe_pros = pd.DataFrame({'company_name':company_names_pros, 'content':pros_text})
     content_dataframe_pros.to_csv("reviews_pro.csv", sep=';', mode = 'a', header = False, index=False)
     
     company_names_cons = [companies[company]] * len(cons_text)
     content_dataframe_cons = pd.DataFrame({'company_name':company_names_cons, 'content':cons_text})
     content_dataframe_cons.to_csv("cons_norway.csv", sep=';', mode = 'a', header = False, index=False)




driver.quit()


# 31/8/17: search again for KPMG. reviews exist