#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 13:11:59 2017

@author: guysimons
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
import pandas as pd
from selenium.webdriver.common.keys import Keys
 
 
def init_driver():

    driver = webdriver.Chrome(executable_path='/Users/guysimons/Documents/JAVA/Webscraping/Drivers/chromedriver')
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

###Linkedin Login###
navigate_page(driver, "https://www.linkedin.com/")
email = driver.find_element_by_name("session_key")
password = driver.find_element_by_name("session_password")
email.send_keys("")
password.send_keys("")

login_button = driver.find_element_by_id("login-submit")
login_button.click()

###Navigate to page
navigate_page(driver, "https://www.linkedin.com/school/5954/")


###Navigate to carreer insights
career_insights = driver.find_element_by_xpath("//div[@class = 'see-all-career-insights-link']/a")
career_insights.click()

###Show more
show_more = driver.find_element_by_xpath("//button[@class='org-alumni-insights__show-more-button Sans-17px-black-55%-semibold']")
show_more.click()

###Get countries
where_they_live = []
where_they_live_values = []

#Make more complex if-statement
for i in range(1,5):
     
     if i == 4:
          next_btn = driver.find_element_by_xpath("//button[@class='next-btn']")
          next_btn.click()
     
     countries_numbers = driver.find_elements_by_xpath("//li"+i+"]//div[@class = 'insight-container']//div[@class='org-bar-graph-element__percentage-bar-info Sans-15px-black-70% mt2 mb4']/strong")
     countries_names = driver.find_elements_by_xpath("//li["+i+"]//div[@class = 'insight-container']//div[@class='org-bar-graph-element__percentage-bar-info Sans-15px-black-70% mt2 mb4']//span")
     for i in countries_names:
          where_they_live.append(i.text)
     
     for j in countries_numbers:
          where_they_live_values.append(j.text)
       
driver.quit()


list_complete = pd.DataFrame({'Rank': ranks, 'University': names, 'Country':countries})
list_complete.to_csv('list.csv', index = False)
