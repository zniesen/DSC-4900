##### Imports ######
import re
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import os
import string

# imports selenium
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Import from seleniumwire
from seleniumwire import webdriver
import numpy as np
import pandas as pd
import json
import requests
import sys
import io

##### import things from my own project
import business_information
import business_navi
import insert_data
import questions_answers
import amenities
import helper_tools
import business_information
from selenium.webdriver.firefox.options import Options

url = "https://www.yelp.com/"
all_amenities = []
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(4)
driver.get(url)  # going to Yelp

user_agent_info = driver.find_element(By.TAG_NAME, "body").text
# print the page content
print(user_agent_info)

next_button = driver.find_element(By.CSS_SELECTOR, "html body yelp-react-root div div.biz-details-page-container-outer__09f24__pZBzx.y-css-mhg9c5 div.biz-details-page-container-inner__09f24__L9S07.y-css-mhg9c5 div.y-css-1ehjqp6 div.y-css-13kng0r main#main-content.y-css-qsv6ye div.y-css-mhg9c5 div#reviews.y-css-mhg9c5 section.y-css-15jz5c7 div.y-css-mhg9c5 div.pagination__09f24__VRjN4.y-css-1l7sbyz div.y-css-mhg9c5 div.pagination-links__09f24__bmFj8.y-css-1n5biw7 div.navigation-button-container__09f24__SvcBh.y-css-mhg9c5 span.y-css-yrt0i5 a.next-link.navigation-button__09f24__m9qRz.y-css-1kw15cs")
def scrape(driver, all_amenities):
    business_info = business_information.getBusinessInfo(driver)
    business_id = business_info["business_id"]
    #insert_data.insert_business(business_id, business_info['business_name'], business_info['

    hours_info = business_information.getHoursInfo(driver)
    insert_data.insert_hours(business_id, hours_info)

    #Amenities
    attributes = amenities.find_amenities(driver, all_amenities)

    pages = range(business_info['Number of Reviews'])

    #Review Handling
    business_reviews = business_information.get_all_reviews(driver, pages, next_button)
    business_information.add_all_reviews(business_reviews, business_id)

    questions_answers.find_all_questions_and_answers(driver, business_id)






    #moving to new page
    business_navi.simple_wander(driver)

    #todo how am I setting business id?
        #  maybe check the value of the last business id and add 1 to that?
        # maybe also have a letter of the alphabet and make it a composite primary key?
        # probably not the best idea bc it will be attached to the others

born2run(driver, all_amenities)


#%%

driver = webdriver.Firefox(options=options)
driver.close()

driver.quit()

