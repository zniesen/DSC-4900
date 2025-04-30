import sqlite3

# Connect to SQLite database (or create one if it doesn't exist)
db_path = "yelp_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create 'business' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS business (
        business_id TEXT PRIMARY KEY,
        business_name TEXT,
        address TEXT,
        phone TEXT,
        rating TEXT,
        num_revs INTEGER,
        website TEXT,
        url TEXT,
        last_scraped DateTime
    )
""")

# Create 'reviews' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        business_id TEXT,
        review_id TEXT,
        review_content TEXT,
        PRIMARY KEY (business_id, review_id),
        FOREIGN KEY (business_id) REFERENCES business (business_id)
    )
""")

# Create 'reviews2' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews2 (
        business_id TEXT,
        review_id TEXT,
        review_content TEXT,
        user_id TEXT,
        rating INTEGER,
        useful INTEGER,
        funny INTEGER,
        cool INTEGER,
        date DateTime,
        PRIMARY KEY (business_id, review_id),
        FOREIGN KEY (business_id) REFERENCES business (business_id)
    )
""")

# Create 'business_hours' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_hours (
        business_id TEXT PRIMARY KEY,
        monday TEXT,
        tuesday TEXT,
        wednesday TEXT,
        thursday TEXT,
        friday TEXT,
        saturday TEXT,
        sunday TEXT,
        FOREIGN KEY (business_id) REFERENCES business (business_id)
    )
""")

# Create 'amenities' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS amenities (
        amenity_name TEXT PRIMARY KEY,
        icon TEXT
    )
""")

# Create 'questions' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        business_id TEXT,
        question_id TEXT,
        question_text TEXT,
        FOREIGN KEY (business_id) REFERENCES business (business_id),
        PRIMARY KEY (business_id, question_id)
    )
""")

# Create 'answers' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        business_id TEXT,
        question_id TEXT,
        answer_id TEXT,
        answer_text TEXT,
        answer_date TEXT,
        helpfulness INTEGER,
        FOREIGN KEY (business_id, question_id) REFERENCES questions (business_id, question_id),
        PRIMARY KEY (business_id, question_id, answer_id)
    )
""")

# Create 'business_amenities' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_amenities (
        business_id TEXT,
        attributes TEXT,
        FOREIGN KEY (business_id) REFERENCES business (business_id),
        PRIMARY KEY (business_id, attributes)
    )
""")

# Create 'unvisited' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS unvisited (
        link TEXT PRIMARY KEY        
    )
""")

# Create 'visited' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS visited (
        link TEXT PRIMARY KEY        
    )
""")

# Commit and close the connection
conn.commit()
conn.close()

print("Database setup complete!")
