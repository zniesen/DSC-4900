#imports
from insert_data import insert_amenity
import sqlite3
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

#functions

#get ongoing list of amenities on yelp
def get_amenities_to_date():
    # connect to the sqlite database
    conn = sqlite3.connect("/Users/zniesen/sensory-space/yelp_data.db")
    cursor = conn.cursor()
    # query to select all amenity names from the amenities table
    query = "SELECT amenity_name FROM `amenities`"
    cursor.execute(query)
    result = cursor.fetchall()
    amenities_list = []
    # append each amenity name to the list
    for i in result: 
        amenities_list.append(i[0])
    return amenities_list

def find_amenities(driver, all_amenities):
    more_amenities_button = driver.find_element(By.CSS_SELECTOR, "section.y-css-15jz5c7:nth-child(8) > div:nth-child(2) > button:nth-child(2)")
    more_amenities_button.click() # load more amenities
    # locate amenities section 
    amenities_section = driver.find_element(By.CSS_SELECTOR, "section.y-css-15jz5c7:nth-child(8) > div:nth-child(2)")
    # find all amenities
    amenities = amenities_section.find_elements(By.CLASS_NAME, "arrange-unit__09f24__rqHTg")
    N = []  # "No" amenity list
    Y = []  # "Yes" amenity list
    
    for amenity in amenities:
        attr_name = amenity.text.strip()  # get amenity name
        if not attr_name:  # skip empty elements
            continue
        if attr_name in all_amenities: continue # check if already listed
        else: all_amenities.append(attr_name)  # add new amenity
        
        try:
            amenity.find_element(By.CLASS_NAME, "y-css-19xonnr")  # check for "No" indicator
            N.append("No" + attr_name)  # add to "No"
        except NoSuchElementException:
            icon = amenity.find_element(By.CLASS_NAME, "y-css-mhg9c5").text  # get icon text
            Y.append(attr_name)  # add to "Yes"
            insert_amenity(attr_name, icon)  # insert into database
            
    return Y + N  # return combined list of amenities
