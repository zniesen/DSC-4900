import sqlite3

# Function to add a business
def insert_business(business_id, business_name, address, phone, rating, num_revs, website, url, last_scraped):
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO business VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (business_id, business_name, address, phone, rating, num_revs, website, url, last_scraped))
    conn.commit()
    conn.close()

def insert_business_amenities(business_id, amenities):
    final_string = ", ".join(amenities)  # Join amenities into a single string
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO business_amenities VALUES (?, ?)
    """, (business_id, final_string))
    conn.commit()
    conn.close()

# Function to add a review
def insert_review(review_id, business_id, review_content):
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()
    # Check if the business exists
    cursor.execute("SELECT business_id FROM business WHERE business_id = ?", (business_id,))
    if cursor.fetchone() is None:
        print(f"Business ID {business_id} not found! Add the business first.")
        conn.close()
        return

    cursor.execute("""
        INSERT OR IGNORE INTO reviews VALUES (?, ?, ?)
    """, (business_id, review_id, review_content))

    conn.commit()
    conn.close()

def insert_amenity(amenity_name):
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO amenities VALUES (?, ?)
    """, (amenity_name, "NULL"))  # Note the comma to make it a tuple
    conn.commit()
    conn.close()

def insert_amenity_and_icon(amenity_name, icon_name):
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO amenities VALUES (?, ?)
    """, (amenity_name, icon_name))  # Note the comma to make it a tuple
    conn.commit()
    conn.close()

def insert_question(business_id, question_id, question_content):
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()

    # Check if the business exists
    cursor.execute("SELECT business_id FROM business WHERE business_id = ?", (business_id,))
    if cursor.fetchone() is None:
        print(f"Business ID {business_id} not found! Add the business first.")
        conn.close()
        return

    cursor.execute("""
        INSERT OR IGNORE INTO questions VALUES (?, ?, ?)
    """, (business_id, question_id, question_content))
    conn.commit()
    conn.close()

def insert_answer(business_id, question_id, answer_id, answer_content, answer_date, helpfulness):
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()

    # Check if the business exists
    cursor.execute("SELECT business_id FROM business WHERE business_id = ?", (business_id,))
    if cursor.fetchone() is None:
        print(f"Business ID {business_id} not found! Add the business first.")
        conn.close()
        return

    cursor.execute("""
        INSERT OR IGNORE INTO answers VALUES (?, ?, ?, ?, ?, ?)
    """, (business_id, question_id, answer_id, answer_content, answer_date, helpfulness))

    conn.commit()
    conn.close()

print("Functions for inserting data are ready to use.")

