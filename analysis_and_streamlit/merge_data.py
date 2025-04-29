import pandas as pd
import glob
import os
import csv
import ast
import time

# Column normalization
column_aliases = {
    'Yelp URL': 'url', 'URL': 'url', 'url': 'url',
    'Reviewer': 'reviewer', 'Rating': 'rating', 'stars': 'rating',
    'Review': 'review_text', 'Review Text': 'review_text', 'text': 'review_text',
    'Date': 'date', 'Time': 'date', 'date': 'date',
    'categoryName': 'category',
    'title': 'title', 'Restaurant': 'title',
    'reviewsCount': 'reviews_count',
    'website': 'website'
}

desired_columns = ['business_id', 'title', 'review_id', 'rating', 'date', 'review_text', 'category', 'from']

def safe_read_csv(file, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return pd.read_csv(file, on_bad_lines='skip', low_memory=False)
        except TimeoutError as te:
            print(f"TimeoutError while reading {file}, retrying in {delay}s... (Attempt {attempt+1}/{retries})")
            time.sleep(delay)
        except Exception as e:
            print(f"Failed to read {file}: {e}")
            return None
    return None

def process_dataframe(df, filename):
    columns_drop = []
    print(f"{filename}: {len(df)} rows")
    print(f"{filename} columns: {df.columns.tolist()}")  # Debugging

    if filename == "1_YelpRestaurantReviews.csv": # from https://www.kaggle.com/datasets/farukalam/yelp-restaurant-reviews
        if 'url' in df.columns:
            df['business_id'] = df['url'].str.extract(r'/biz/([^/?#]+)')[0].fillna('unknown')
            df['title'] = df['business_id'].str.replace('-', ' ', regex=False).str.title()
        else:
            print(f"{filename} missing 'url' column — assigning generic business_id.")
            df['business_id'] = 'unknown'
        df['category'] = "Restaurant"

    elif filename == "2_10000Restaurantreviews.csv": # from https://www.kaggle.com/datasets/joebeachcapital/restaurant-reviews
        df['business_id'] = df.get('restaurant', pd.Series("unknown")).astype(str).str.replace(" ", "-").str.lower()
        columns_drop = ['Restaurant', 'Pictures', 'Metadata', 'Reviewer', '']
        df['category'] = "Restaurant"

    elif filename == "Yelp_academic_reviews.csv": #From Yelp API
        df.rename(columns={'stars': 'rating'}, inplace=True)
        columns_drop = ['user_id', 'funny', 'cool', 'useful']
        df = df.merge(yelp_business_df, on="business_id", how="left")
        df['category'] = df['categories']
        df['title'] = df['name']
        df.drop(columns=['name', 'categories'], inplace=True)  # if you copy to 'title', 'category'


    elif "google" in filename.lower(): # from https://www.kaggle.com/datasets/denizbilginn/google-maps-restaurant-reviews
        df['business_id'] = df.get('title', pd.Series("unknown")).astype(str).str.replace(" ", "-").str.lower()
        columns_drop = ['url', 'website', 'reviews_count']

    elif filename == "5_TripAdvisor.csv": # from https://www.kaggle.com/datasets/andrewmvd/trip-advisor-hotel-reviews -- removed due to lack of title information
        def extract_overall_rating(ratings_str):
            try:
                rating_dict = ast.literal_eval(ratings_str)
                return rating_dict.get('overall')
            except Exception:
                return None

        df['rating'] = df['ratings'].apply(extract_overall_rating)
        df['review_id'] = df.get('id', pd.Series(pd.NA))
        df['review_text'] = df['review_text']
        df['business_id'] = df.get('offering_id', 'unknown')
        df['category'] = 'Hotel'  # or "Restaurant" depending on your needs
        columns_drop = ['ratings', 'via_mobile', 'author', 'offering_id', 'title', 'num_helpful_votes', 'date_stayed']

    # Ensure business_id exists before grouping
    if 'business_id' not in df.columns or df['business_id'].isnull().all():
        print(f"{filename} has no valid business_id! Assigning fallback ID.")
        df['business_id'] = 'unknown'

    if 'review_id' not in df.columns:
        df['review_id'] = df.groupby('business_id').cumcount() + 1

    if 'from' not in df.columns:
        df['from'] = filename

    if columns_drop:
        df.drop(columns=columns_drop, errors='ignore', inplace=True)

    for col in desired_columns:
        if col not in df.columns:
            print(f"{filename} missing column: {col}")
            df[col] = pd.NA

    return df[desired_columns]

def process_single_file(file, output_file, first_file):
    df = safe_read_csv(file)
    if df is None:
        print(f"Skipping {file} due to read error.")
        return False

    filename = os.path.basename(file)
    df = df.rename(columns={col: column_aliases.get(col, col) for col in df.columns})
    df = process_dataframe(df, filename)

    if df.empty:
        print(f"{filename} resulted in an empty DataFrame, skipping.")
        return False

    print(f"{filename} writing {len(df)} rows to CSV...")
    df.to_csv(output_file, mode='a', index=False, header=first_file, quoting=csv.QUOTE_MINIMAL)
    return True

if __name__ == "__main__":
    path = r"PATH"
    output_file = 'merged.csv'
    processed_sources = set()
    print("Looking for CSV files in:", path)
    files = glob.glob(os.path.join(path, "*.csv"))
    print("Found files:", files)
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_csv(output_file, usecols=["from"], low_memory=False)
            processed_sources = set(existing_df["from"].dropna().unique())
            print(f"Already processed sources: {processed_sources}")
        except Exception as e:
            print(f"Could not read existing file: {e}")

    first_file = not os.path.exists(output_file)

    yelp_business_df = pd.read_csv("PATH", usecols=["business_id", "name", "categories"])

    for file in glob.glob(os.path.join(path, "*.csv")):
        filename = os.path.basename(file)
        if filename in processed_sources:
            print(f"Skipping already processed file: {filename}")
            continue

        print(f"Processing {file}")
        success = process_single_file(file, output_file, first_file)
        if success and first_file:
            first_file = False
