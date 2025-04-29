#todo: for related businesses we may want to remove the extra stuff at the end :',(
# https://www.yelp.com/biz/honky-tonk-the-twelve-thirty-club-nashville?page_src=related_bizes
# so only save up to the ?
import sqlite3
from selenium.webdriver.common.by import By

######################################################################################################
conn = sqlite3.connect("yelp_data.db")
cursor = conn.cursor()
conn = sqlite3.connect("yelp_data.db")
cursor = conn.cursor()

def insert_unvisited(link):
    conn = sqlite3.connect("yelp_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO unvisited VALUES (?)
    """, (link))  # Note the comma to make it a tuple
    conn.commit()
    conn.close()

def insert_visited(link):
    conn = sqlite3.connect("yelp_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO visited VALUES (?)
    """, (link))  # Note the comma to make it a tuple
    conn.commit()
    conn.close()

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

def get_unvisited_to_date():
    conn = sqlite3.connect("yelp_data.db")
    cursor = conn.cursor()
    query = "SELECT link FROM `unvisited`"
    cursor.execute(query)
    result = cursor.fetchall()
    unvisited_list = []
    for i in result: unvisited_list.append(i[0])
    return unvisited_list
def get_visited_to_date():
    conn = sqlite3.connect("yelp_data.db")
    cursor = conn.cursor()
    query = "SELECT link FROM visited"
    cursor.execute(query)
    result = cursor.fetchall()
    visited_list = []
    for i in result: visited_list.append(i[1])
    return visited_list
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
        link = get_rec_business_url_and_id(raw_url, False)
        if link in visited:
            return
        else:
            chosen_link = link
            chosen_thing = thing
            if link not in unvisited:
                insert_unvisited(link)
                recs.append(chosen_link)
    return chosen_thing, recs



    # todo finish this
                # return button to click

    #check if in not visited list
def get_rec_business_url_and_id(raw_url, want_id):
    clean_url = raw_url.split('?')
    if want_id:
        id = clean_url[0].replace('https://www.yelp.com/biz/', '')
        return clean_url[0], id
    else:
        return clean_url[0]
def simple_wander(driver):
    chosen_one, recs = extractRecommendedUrls(driver)
    insert_visited(get_rec_business_url_and_id(driver.current_url(), False))
    chosen_one.click()
def wander(driver):
    chosen_one, recs = extractRecommendedUrls(driver)
    get_rec_business_url_and_id(driver.current_url(), False)
    #continue later
    chosen_one.click()


    #get all
    return


# y-css-1ia85zx
# To Do:
# - todo extractRecommendedUrls(business_info)
# - todo saving things to sql tables
# - todo move on to Recommended location
# - todo set up crawling logic and data saving for Recommended locations




# To Do:
# - todo extractRecommendedUrls(business_info)
# - todo saving things to sql tables
# - todo move on to Recommended location
# - todo set up crawling logic and data saving for Recommended locations