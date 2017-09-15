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
from selenium.common.exceptions import NoSuchElementException
from time import sleep  

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

# new problem with the loop. when chekcing the browswer I can see that it looks at different companies, but allways the first page.
for item in companies:
    print("Retrieving data for ", item)
    
    #Create lists to store reviews of current company (item)
    rev_comp = []
    pros_comp = []
    cons_comp = []
    
    #not sure if this is the easiest way. url is www.indeeed.com/name-of-company. slash btw words need to be added

    #input company name in search field
    navigate_page(driver, "https://www.indeed.com/Best-Places-to-Work")
    
    # Save the window opener (current window, do not mistaken with tab... not the same)
    #main_window = driver.current_window_handle

    
    #inputElement = driver.find_element_by_text("Enter a company name")
    inputElement = driver.find_element_by_id("search-by-company-input") #the id changes depending on the page that is loaded. -input-header is sometimes added
    inputElement.send_keys(item)
    inputElement.send_keys(Keys.ENTER) 
    
    # Put focus on current window which will, in fact, put focus on the current visible tab
    #driver.switch_to_window(main_window)                      

    rev_btn = driver.find_element_by_xpath("//div[@class='cmp-tile-footer-element']/a[@data-tn-element='reviews-footer-link']")
    #rev_btn.send_keys(Keys.COMMAND + 't') #to open link in new tab
    rev_btn.click()
    # ERROR: It looks like it doesn't click on the reviews button for a new company, but goes back to the review page of the first company.
    
    # Switch tab to the new tab, which we will assume is the next one on the right
    #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    
    print ("wait 10s for page to load")
    driver.wait = WebDriverWait(driver, 10) 
    
    #create text files to store results
    #with open ("reviews/text_"+item+".txt", "w", encoding='utf8') as text_out, open("reviews/pros_"+item+".txt", "w", encoding='utf8') as pro_out, open("reviews/cons_"+item+".txt", "w", encoding='utf8') as con_out:
    while True: #
        
        # grap the reviews and store in datafile w/ name = item
        #for all pages ()
        
        #print current page number
        page_number = driver.find_element_by_xpath("//span[@class='company_reviews_pagination_link bolder']").text #adapt id to page
        print ("page # ", page_number) # to help me keep track of progress
        
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
        

        #why have here a command to go to the next page and then again in the try-except block? If I take it out the driver stays on page 1
        try:
            next_btn = driver.find_element_by_xpath("//a[@data-tn-element='next-page']/span")
            #next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '*[contains(@class, "company_reviews_pagination_link_nav")]//span[. = "next-page"]')))
            #if the line above includes an explicit wait, it doesn't go to the next page
            next_btn.click()
        except:
            print ("end of reviews , try-except 1") #w/ page 1 etc. the try is successful

        try:
            print ("check if new page")
            #I think the XPATH is wrong
            #next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-tn-element='next-page']/span")))
            next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '*[contains(@class, "company_reviews_pagination_link_nav")]//a[. = "next-page"]')))
            #next_btn = driver.find_element_by_xpath("//a[@data-tn-element='next-page']/span") #this doesn't work. gives error stale element
            next_btn.click()
        except: # NoSuchElementException: 
            print ("end of reviews, try_except 2")

        #text_out.close, pro_out.close, con_out.close
        #this is reopening the files to append the data. files so far not closed

    print ("store eth in txt files")
    with open ("reviews/text_"+item+".txt", "w", encoding='utf8') as text_out:
        #for i in range(0, len(txt_rev)):
         #   rev_comp.append(txt_rev[i].text)
         text_out.write(str(rev_comp))
            
    with open("reviews/pros_"+item+".txt", "w", encoding='utf8') as pro_out:
    #for i in range(0, len(pros)):
     #   pros_comp.append(pros[i].text)
         pro_out.write(str(pros_comp))
        
    with open("reviews/cons_"+item+".txt", "w", encoding='utf8') as con_out:
    #for i in range(0, len(cons)):
    #    cons_comp.append(cons[i].text)
        con_out.write(str(cons_comp))
    
    '''
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
    '''
                

driver.quit()