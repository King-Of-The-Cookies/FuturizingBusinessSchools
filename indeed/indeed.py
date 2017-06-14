#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:48:19 2017

@author: katerinadoyle
@author: Guy Simons
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import csv
import pandas as pd

def init_driver():

    #driver = webdriver.Chrome(executable_path='/Users/guysimons/Documents/JAVA/Webscraping/Drivers/chromedriver')
    #driver = webdriver.Chrome(executable_path='/Users/katerinadoyle/Documents/java/webscraping/drivers/chromedriver')
    driver = webdriver.Firefox(executable_path='/Users/katerinadoyle/Documents/java/webscraping/drivers/geckodriver')
    driver.wait = WebDriverWait(driver, 5)
    driver.implicitly_wait(10)
    return driver

def navigate_page(driver, page):
     driver.get(page)          
 
def lookup(driver, query):
    try:
        element = driver.find_element_by_xpath(query).text
        return element
    except:
          print("An error occured, the element doesn't exist")

driver = init_driver()
wait = WebDriverWait(driver, 10) #explicit waits
 
# indeed only has 50 companies listed on 2 pages. this was quickest way to get all the companies
links = ["https://www.indeed.com/Best-Places-to-Work", 
"https://www.indeed.com/Best-Places-to-Work?y=2017&cc=US&start=25"]

#get values of Select(driver.find_element_by_xpath("//div[@id = 'cmp-discovery-country-select']/select"))

companies = [ ]

for item in links:
    navigate_page(driver, item)

    # select the country. Include this in another for-loop? for item in country
    select = Select(driver.find_element_by_xpath("//div[@id = 'cmp-discovery-country-select']/select"))
    select.by_value = ('United States' )

    company_name = driver.find_elements_by_xpath("//div[@id = 'cmp-curated']/div/a/h4[@itemprop='name']")
    for i in range (0, len(company_name)):
        companies.append(company_name[i].text)

    # select the reviews. 

#driver.quit()

#companies = pd.read_csv("companies_indeed_leaderboard.csv", names=["company"], header=0)

#driver = init_driver()


for item in companies:
    rev_comp = []
    pros_comp = []
    cons_comp = []
    #name_slice = item. not sure if this is the easiest way. url is www.indeeed.com/name-of-company. slash btw words need to be added

    #input company name in search field
    #select reviews
    navigate_page(driver, "https://www.indeed.com/Best-Places-to-Work")
    
    inputElement = driver.find_element_by_id("search-by-company-input")
    inputElement.send_keys(item)
    inputElement.send_keys(Keys.ENTER)

    rev_btn = driver.find_element_by_xpath("//div[@class='cmp-tile-footer-element']/a[@data-tn-element='reviews-footer-link']")
    rev_btn.click()
    
    print ("wait 10s for page to load")
    
    driver.wait = WebDriverWait(driver, 10) 
    
    #create text files to store results
    with open ("reviews/text_"+item+".txt", "w", encoding='utf8') as text_out, open("reviews/pros_"+item+".txt", "w", encoding='utf8') as pro_out, open("reviews/cons_"+item+".txt", "w", encoding='utf8') as con_out:
        text_out.close, pro_out.close, con_out.close
        
        while True: #
        
        # grap the reviews and store in datafile w/ name = item
        # currently only does 1st page. Need to create loop also for this? Or better way
        #for all pages ()
            
            txt_rev = driver.find_elements_by_xpath("//span[@class='cmp-review-text']")
            print ("text found")
            pros = driver.find_elements_by_xpath("//div[@class='cmp-review-pro-text']")
            print ("pros found" )
            cons = driver.find_elements_by_xpath("//div[@class='cmp-review-con-text']")
            print ("cons found")
            
            
            # store output
            print ("begin storing")
            for i in range(0, len(txt_rev)):
                rev_comp.append(txt_rev[i].text)
            print ("stored text in rev_comp")
            for i in range(0, len(pros)):
                pros_comp.append(pros[i].text)
            print ("stored pros in pros_comp")
            for i in range(0, len(cons)):
                cons_comp.append(cons[i].text)
            print ("stored cons in cons_comp")
                    
            print ("page done, go to next") 
            
            
            txt_rev = []
            pros = [ ]
            cons = [ ]
            
            #this is reopening the files to append the data. files so far not closed
            with open ("reviews/text_"+item+".txt", "a", encoding='utf8') as output:
                #for i in range(0, len(txt_rev)):
                 #   rev_comp.append(txt_rev[i].text)
                 text_out.write(str(rev_comp))
                    
            with open("reviews/pros_"+item+".txt", "a", encoding='utf8') as output:
            #for i in range(0, len(pros)):
             #   pros_comp.append(pros[i].text)
                 pro_out.write(str(pros_comp))
                
            with open("reviews/cons_"+item+".txt", "a", encoding='utf8') as output:
            #for i in range(0, len(cons)):
            #    cons_comp.append(cons[i].text)
                con_out.write(str(cons_comp))
            
            next_btn = driver.find_element_by_xpath("//a[@data-tn-element='next-page']/span")
            next_btn.click() 
            
            #element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[@class='cmp-review-text']")))
            ''' 
            #this block of try except code returned a stale element exception
            try:
                next_btn = driver.find_element_by_xpath("//a[@data-tn-element='next-page']/span")
                next_btn.click()
            except TimeoutException:
                next
            '''
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '*[contains(@class, "reviews_pagination_link_nav")]//span[. = "next-page"]')))
                element.click()
            except: 
                break
                #throws exception NoSuchElementException on the last page and ends the program. 
            
driver.quit()

#next_btn = driver.find_element_by_xpath("//span[@class='cmp-paginator-page']/a[. ='2']")
#next_btn.click()

#driver = init_driver()
#navigate_page(driver, "https://www.indeed.com/Best-Places-to-Work")


# get names of all companies
'''
for i in range(1, 50):
    
#    if i == 25:    
    next_btn = driver.find_element_by_xpath("//span[@class='cmp-paginator-page']/a[. ='2']")
    next_btn.click()

    company_name = driver.find_elements_by_xpath("//div[@id = 'cmp-curated']/div/a/h4[@itemprop='name']")

    for i in range (0, len(company_name)):
    companies.append(company_name1[i].text)
'''

'''
re.findall('/cmp/?/reviews', response)

for i in range (1, xx): (range of companies)
select reviews page. link to review page always /cmp/name-of-company/reviews
scrape text reviews

# store reviews in data set
    
    

ranks = []
names = []
countries = []

for i in range(1,101):
     rank = str(i)
     ranks.append(lookup(driver, "//*[@id='rankings_mod']/div["+ rank +"]//span[1]"))
     names.append(lookup(driver, "//*[@id='rankings_mod']/div["+ rank +"]//span[2]"))
     countries.append(lookup(driver, "//*[@id='rankings_mod']/div["+ rank +"]//span[3]"))




list_complete = pd.DataFrame({'Rank': ranks, 'University': names, 'Country':countries})
list_complete.to_csv('list.csv', index = False)

''' 
