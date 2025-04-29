# Imports
from datetime import time

# Selenium
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Local
import helper_tools
from insert_data import insert_answer, insert_question

def go_to_next_question_page(driver):
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".icon--24-chevron-right-v2"))
        )
        next.click()
        time.sleep(3)  # Wait for page to load
        return True
    except:
        return False  # No next button found, stop

def checkforanswers(driver, business_id, question_id, question_element):
    try:
        # Check if "No answers yet." exists
        if "No answers yet." in question_element.text:
            return 0

        # Check if "See more answers" exists #todo fix check for answers and make it try statements
        see_more_answers = question_element.find_elements(By.CLASS_NAME, "y-css-t4g9e1")
        if see_more_answers:
            see_more_answers[0].click()  # Expand answers
            time.sleep(2)

        # Extract answers
        answers = question_element.find_elements(By.CSS_SELECTOR, "li.y-css-indvim")  # Update selector
        num_answers = len(answers)

        answer_counter = 0
        for answer in answers:
            answer_text = answer.find_element(By.CSS_SELECTOR, "p").text  # Update selector
            answer_id = answer_counter
            answer_counter += 1
            time_posted = answer.find_element(By.CLASS_NAME, " y-css-1d8mpv1").text  # Update selector

            updownvotes = answer.find_elements(By.CLASS_NAME, "y-css-1ickgui")
            helpfulness = helper_tools.convert_to_number(updownvotes[0].text) - helper_tools.convert_to_number(updownvotes[1].text)

            # Insert into answers table
            insert_answer(business_id, question_id, answer_id, answer_text, time_posted, helpfulness)
        return num_answers
    except Exception as e:
        print(f"Error checking answers: {e}")
        return 0

def find_all_questions_and_answers(driver, business_id):
    question_counter = 0
    while True:  # Loop through pages
        question_elements = driver.find_elements(By.CSS_SELECTOR, "li.y-css-indvim")

        for question_element in question_elements:
            try:
                question_id = question_counter
                question_counter += 1
                question_text = question_element.find_element(By.CSS_SELECTOR, "p").text  # Extract question text
                num_answers = checkforanswers(question_element, question_id)
                # Store in database
                insert_question(business_id, question_id, question_text, num_answers)
            except Exception as e:
                print(f"Error extracting question: {e}")

        # Go to the next page of questions
        try:
            next_q_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.icon--24-chevron-right-v2')))
            next_q_page.click()
            time.sleep(3)  # Wait for page load
        except:
            break  # Stop if no more pages



