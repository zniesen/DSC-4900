#imports
import datetime
from datetime import time
from dateutil.utils import today
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import helper_tools
import insert_data
from helper_tools import no_numbers
import sqlite3

# Scrape basic business information
def getBusinessInfo(driver):
    # initialize a dictionary to hold business info
    business_info = {'BusinessID': (helper_tools.get_business_url_and_id(driver, True))[1],
                     'Name': None,
                     'Address': None,
                     'Location': None,
                     'Phone': None,
                     'Rating': None,
                     'Number of Reviews': None,
                     'Website': None,
                     'URL': (helper_tools.get_business_url_and_id(driver, False)),
                     'Last Updated': datetime.datetime.now()}

    # find business name
    name_tag = driver.find_element(By.CSS_SELECTOR,
                                   '.y-css-olzveb').text  # Replace with the actual class of the business name element on Yelp
    if name_tag:
        business_info['Name'] = name_tag

    # find business address
    address_tag = driver.find_element(By.CSS_SELECTOR,
                                      '.y-css-1wktqmn > a:nth-child(1) > span:nth-child(1)').text + driver.find_element(
         By.CSS_SELECTOR, 'p.y-css-229kp8:nth-child(2) > span:nth-child(1)').text
    if address_tag:
        business_info['Address'] = address_tag

    location_tag = driver.find_element(By.XPATH, '/html/body/yelp-react-root/div[1]/div[8]/div/div[1]/div[1]/main/div[2]/section/div[2]/div[1]/div/div/div/div[1]/address/p[2]/span')
    if location_tag:
        business_info['Location'] = no_numbers(location_tag.text)

    # find business phone number
    phone_tag = driver.find_element(By.CSS_SELECTOR,
                                    'div.y-css-4cg16w:nth-child(2) > div:nth-child(1) > div:nth-child(2) > p:nth-child(2)')  # Replace with the actual class of the phone number element on Yelp
    if phone_tag:
        business_info['Phone'] = phone_tag.text

    # find overall business rating
    rating_tag = driver.find_element(By.CSS_SELECTOR,
                                     'div.gutter-1-5__09f24__vMtpw:nth-child(2) > div:nth-child(2) > span:nth-child(1)').text  # div.gutter-1-5__09f24__vMtpw:nth-child(2) > div:nth-child(2) > span:nth-child(1) # Replace with the actual class of the rating element on Yelp
    if rating_tag:
        business_info['Rating'] = rating_tag

    # find number of reviews
    review_count_tag = driver.find_element(By.CSS_SELECTOR,
                                           '.y-css-r8orer > a:nth-child(1)').text  # Replace with the actual class of the review count element on Yelp
    if review_count_tag:
        review_text = review_count_tag
        business_info['Number of Reviews'] = helper_tools.convert_to_number(review_text)  # Extract digits from the review count text


    # find external website if it exists
    website_tag = driver.find_element(By.CSS_SELECTOR,
                                      'div.y-css-4cg16w:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(2) > a:nth-child(1)')
    if website_tag:
        business_info['Website'] = website_tag.text

    business_info['Last Updated'] = today()

    return business_info

# %%
# Scrape hours info
def getHoursInfo(driver, business_id):
    hours_info = {
        'Mon': None,
        'Tue': None,
        'Wed': None,
        'Thu': None,
        'Fri': None,
        'Sat': None,
        'Sun': None,
    }

    mon_tag = driver.find_element(By.CSS_SELECTOR,
                                  'tr.y-css-29kerx:nth-child(2) > td:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > p:nth-child(1)').text
    if mon_tag:
        hours_info['Mon'] = mon_tag

    tue_tag = driver.find_element(By.CSS_SELECTOR,
                                  'tr.y-css-29kerx:nth-child(4) > td:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > p:nth-child(1)').text
    if tue_tag:
        hours_info['Tue'] = tue_tag

    wed_tag = driver.find_element(By.CSS_SELECTOR,
                                  'tr.y-css-29kerx:nth-child(6) > td:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > p:nth-child(1)').text
    if wed_tag:
        hours_info['Wed'] = wed_tag

    thu_tag = driver.find_element(By.CSS_SELECTOR,
                                  'tr.y-css-29kerx:nth-child(8) > td:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > p:nth-child(1)').text
    if thu_tag:
        hours_info['Thu'] = thu_tag

    fri_tag = driver.find_element(By.CSS_SELECTOR,
                                  'tr.y-css-29kerx:nth-child(10) > td:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > p:nth-child(1)').text
    if fri_tag:
        hours_info['Fri'] = fri_tag

    sat_tag = driver.find_element(By.CSS_SELECTOR,
                                  'tr.y-css-29kerx:nth-child(12) > td:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > p:nth-child(1)').text
    if sat_tag:
        hours_info['Sat'] = sat_tag

    sun_tag = driver.find_element(By.CSS_SELECTOR,
                                  'tr.y-css-29kerx:nth-child(14) > td:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > p:nth-child(1)').text
    if sun_tag:
        hours_info['Sun'] = sun_tag


    conn = sqlite3.connect("yelp_data2.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO business_hours VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (business_id, hours_info['Mon'], hours_info['Tues'], hours_info['Wed'], hours_info['Thu'], hours_info['Fri'], hours_info['Sat'], hours_info['Sun']))
    conn.commit()
    conn.close()
    return hours_info

# %%
# review scraping functions
def get_page_reviews(driver, business_reviews):
    # find reviews on page
    reviews = driver.find_elements(By.CLASS_NAME, 'raw__09f24__T4Ezm')
    # adds reviews to all_reviews if there is not one already there
    for review in reviews:
        if review in business_reviews:
            continue
        else:
            business_reviews.append(review) #todo figure out where/when you want to add review to sqllite
        print(review.text)

def go_to_next_question_page(driver):
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                          "html body yelp-react-root div div.biz-details-page-container-outer__09f24__pZBzx.y-css-mhg9c5 div.biz-details-page-container-inner__09f24__L9S07.y-css-mhg9c5 div.y-css-1ehjqp6 div.y-css-13kng0r main#main-content.y-css-qsv6ye div.y-css-mhg9c5 div#reviews.y-css-mhg9c5 section.y-css-15jz5c7 div.y-css-mhg9c5 div.pagination__09f24__VRjN4.y-css-1l7sbyz div.y-css-mhg9c5 div.pagination-links__09f24__bmFj8.y-css-1n5biw7 div.navigation-button-container__09f24__SvcBh.y-css-mhg9c5 span.y-css-yrt0i5 a.next-link.navigation-button__09f24__m9qRz.y-css-1kw15cs"))
        )
        next_button.click()
        time.sleep(3)  # Wait for page to load
        return True
    except:
        return False  # No next button found, end pagination

def get_all_reviews(driver, pages, business_id): #todo figure out where/when you want to add review to sqllite
    business_reviews = []
    for i in range(pages): # todo is pages the right type for this to work?
        get_page_reviews(driver, business_reviews)
        go_to_next_question_page(driver) #is this right?
        add_all_reviews(business_reviews, business_id)
    return business_reviews

def add_all_reviews(business_reviews, business_id):
    review_id = 0
    for i in business_reviews:
        review_id += 1
        insert_data.insert_review(review_id, business_id, i)
    print("all reviews added")
