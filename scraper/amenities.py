#imports
from insert_data import insert_amenity
import sqlite3
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

#functions
def get_amenities_to_date():
    conn = sqlite3.connect("/Users/zniesen/sensory-space/yelp_data.db")
    cursor = conn.cursor()
    query = "SELECT amenity_name FROM `business_amenities`"
    cursor.execute(query)
    result = cursor.fetchall()
    amenities_list = []
    for i in result: amenities_list.append(i[0])
    return amenities_list
def find_amenities(driver, all_amenities):
    more_amenities_button = driver.find_element(By.CSS_SELECTOR, "section.y-css-15jz5c7:nth-child(8) > div:nth-child(2) > button:nth-child(2)")
    more_amenities_button.click()
    amenities_section = driver.find_element(By.CSS_SELECTOR, "section.y-css-15jz5c7:nth-child(8) > div:nth-child(2)")
    amenities = amenities_section.find_elements(By.CLASS_NAME, "arrange-unit__09f24__rqHTg")
    N = []
    Y = []
    for amenity in amenities:
        attr_name = amenity.text.strip()  # Extract and clean text
        #icon = amenity.find_element(By.CLASS_NAME, "y-css-mhg9c5").text

        if not attr_name:  # Skip empty elements
            continue
        if attr_name in all_amenities:
            continue
        else:
            all_amenities.append(attr_name)
        try:
            # Check if the element exists
            amenity.find_element(By.CLASS_NAME, "y-css-19xonnr")
            N.append("No" + attr_name)
        except NoSuchElementException:
            icon = amenity.find_element(By.CLASS_NAME, "y-css-mhg9c5").text
            Y.append(attr_name)
            insert_amenity(attr_name, icon)
    return Y + N


    #amenities = driver.find_elements(By.class, "arrange-unit__09f24__rqHTg y-css-mhg9c5")
    #amenities = driver.find_elements(By.CSS_SELECTOR, "div.arrange-unit__09f24__rqHTg:nth-child(16) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)")
    #amenities = driver.find_elements(By.CSS_SELECTOR, "arrange-unit__09f24__rqHTg y-css-mhg9c5")
    #for amenity in amenities:
        #attr_name = amenity.text
        #try: driver.find_element(By.CLASS_NAME, "y-css-19xonnr")

#%%
# """
# from selenium import webdriver
#
# #test
# url = "https://www.yelp.com/biz/milk-and-honey-nashville?osq=Restaurants"
# all_amenities = []
#
# url = "https://www.yelp.com/biz/skulls-rainbow-room-nashville?page_src=related_bizes"
# driver = webdriver.Firefox() #the webdriver
# driver.implicitly_wait(2)
# driver.get(url) #going to Yelp
#
# find_amenities(driver, all_amenities)
# """
#%%

# "div.arrange-unit__09f24__rqHTg:nth-child(10) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)"
# "div.arrange-unit__09f24__rqHTg:nth-child(29) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)"
# "div.arrange-unit__09f24__rqHTg:nth-child(31) > div:nth-child(1) > div:nth-child(1)"
# "div.arrange-unit__09f24__rqHTg:nth-child(8) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)"
# "div.arrange-unit__09f24__rqHTg:nth-child(30)"
#body > div.l-wrapper > main > div.panel-collection > section.panel.s-wrapper.site-panel.s-wrapper--no-padding.site-panel--textgrid.yelp-textgrid-image--large.yelp-textgrid--layout_list > div > div > div > div > div:nth-child(1) > div > div.yelp-textgrid-feature__title.h2

#%%
#css=.icon--24-ada-compliant-restroom-v2
    #css=.icon--24-ada-compliant-restroom-v1??
#css=.icon--24-accessible-parking-v2
#driver.quit()



#%%
#print(all_amenities)