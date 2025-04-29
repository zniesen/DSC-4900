#imports
import sqlite3
from selenium.webdriver.common.by import By
from helper_tools import 

conn = sqlite3.connect("yelp_data.db")
cursor = conn.cursor()
conn = sqlite3.connect("yelp_data.db")
cursor = conn.cursor()

#insert the link of an unscraped location to unvisited 
def insert_unvisited(link):
    conn = sqlite3.connect("yelp_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO unvisited VALUES (?)
    """, (link))  # Note the comma to make it a tuple
    conn.commit()
    conn.close()

#insert the link of a scraped location to visited 
def insert_visited(link):
    conn = sqlite3.connect("yelp_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO visited VALUES (?)
    """, (link))  # Note the comma to make it a tuple
    conn.commit()
    conn.close()

#transfer link from unvisited to visited
def transfer_unvisited(link):
    conn = sqlite3.connect("yelp_data.db")
    cursor = conn.cursor()
    # Check if the record exists in the source table
    cursor.execute(f"SELECT * FROM unvisited WHERE link = ?", (link))
    record = cursor.fetchone()

    if record:
        # Insert the record into the target table
        cursor.execute(f"INSERT OR IGNORE INTO visited VALUES (?)", (link))
        conn.commit()

    cursor.execute("""INSERT OR IGNORE INTO visited VALUES (?)
    """, (link))  # Note the comma to make it a tuple
    cursor.execute(f"DELETE FROM unvisited WHERE link = ?", (link))
    conn.commit()
    conn.close()

#get current unvisited as a list
def get_unvisited_to_date():
    conn = sqlite3.connect("yelp_data.db")
    cursor = conn.cursor()
    query = "SELECT link FROM `unvisited`"
    cursor.execute(query)
    result = cursor.fetchall()
    unvisited_list = []
    for i in result: unvisited_list.append(i[0])
    return unvisited_list
    
#get current visited as a list
def get_visited_to_date():
    conn = sqlite3.connect("yelp_data.db")
    cursor = conn.cursor()
    query = "SELECT link FROM visited"
    cursor.execute(query)
    result = cursor.fetchall()
    visited_list = []
    for i in result: visited_list.append(i[1])
    return visited_list

#scrape the urls of locations in the recommended section at the bottom of a Yelp page
def extractRecommendedUrls(driver):
    ppl_also_viewed = driver.find_element(By.CSS_SELECTOR,
                                              ".carousel-container__09f24__sm9Zt > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
    more_locs = ppl_also_viewed.find_elements(By.CLASS_NAME, "y-css-1ia85zx")
    visited = get_visited_to_date()
    unvisited = get_unvisited_to_date()
    recs = []
    for i in more_locs:
        thing = more_locs.find_element(By.CLASS, " y-css-12x5mn4")
        raw_url = thing.get_attribute("href")
        link = helper_tools.get_rec_business_url_and_id(raw_url, False)
        if link in visited:
            return
        else:
            chosen_link = link
            chosen_thing = thing
            if link not in unvisited:
                insert_unvisited(link)
                recs.append(chosen_link)
    return chosen_thing, recs

# move to an unvisited recommended location
def simple_wander(driver):
    chosen_one, recs = extractRecommendedUrls(driver)
    insert_visited(get_rec_business_url_and_id(driver.current_url(), False))
    chosen_one.click()
