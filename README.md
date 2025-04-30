# DSC-4900 Final Project
# Accessibility Review Analysis
  - Start date: 01/2024
  - DSC-4900 - Data Science Project and Portfolio @ Belmont University
  - Author: Zoe Niesen

Table of Contents
---
   * [About the project](#about-the-project)
   * [Database Creation](#database-creation)
   * [Web Scraper](#scraping-data-from-yelp)
      * [Step 1: Initialize SQL Database](#step-1-initialize-sql-database)
      * [Step 2: Collect some business links](#step-2-collect-some-business-links) 
      * [Step 3: Run scraper on your link](#step-3-run-scraper-on-your-link)
   * Analysis and Recommendations](#analysis-and-recommendations)
      * [Review Analysis](#review-analysis)
      * [Content-based Recommendation](#content-based-recommendation)
      * [Screenlit Recommendation App](#screenlit-recommendation-app)
   * [IRB](#irb)
      * [IRB Proposal](#irb-proposal)


## About the project
This project was originally for my data science independent studies and the course, DSC-4900, at Belmont University. I intend to continue applying what I have learned as I progress in my career and continue work on this. Currently, my progress is:
 - 1. Built a web scraping protocol to collect information from Yelp reviews, questions and answers, [COMEBACK]
 - 2. Review Analysis using NLP and data from the Yelp API to rate businesses on customer perception of accessibility as indicated by reviews.
 - 3. Built a recommendation system and simple UI that suggests businesses based on indicated accessibility needs
 - 4. Wrote an IRB proposal to continue research using feedback from disabled populations

##Languages Used
- Python
- SQL
- Javascript
- CSS

## Database Creation

## Scraping data from Yelp
Here are the steps involved in my Yelp-Scraping Protocol

### Step 1: Initialize SQL Database

### Step 2: Get a starting link

#### a) Find a business you want to start with 
```
python scraper/scrape.py
```

## Data Analysis, Recommendations, User Interface
### Dataset Information
Dataset Information
The dataset comprises a mix of:
- Previously scraped data (before Yelp's security escalation)
- Manually scraped data
- Yelp API responses
- Public Kaggle datasets

### Merged Data Dictionary
The datasets are merged using LINK TO CODE HERE, which produces "merged.csv", a csv with the following columns:
| Column | Description |
|--------|-------------|
| `business_id` | A unique identifier for each business, either provided in the dataset, or produced using the business name or part of the review site url|
| `title` | The name of the location |
| `review_id` | An identifier for each review either provided in the dataset, **or produced by counting upwards and reseting for each business ** COME BACK|
| `date` | a value representing the date scraped or the date the review was posted, depending on the dataset. It is included to offer an approximation of how up-to-date the information provided in the review is|
| `review_text` | the review content|
| `category` | **come back** |
| `from` | the dataset the review came from |

### Data Analysis
This section covers the methodology for analyzing business reviews to assess accessibility features and sentiment trends using Natural Language Processing (NLP).
#### Accessibility Analysis Overview
The system processes review text to identify keywords related to accessibility features such as mobility accommodations, visual impairments, auditory sensitivity, and more. Sentiment analysis is applied to quantify positive, neutral, and negative experiences for each business.
##### Processing Steps
- **Extract Accessibility Keywords**: Using precompiled regex patterns, the script identifies relevant accessibility terms from business reviews.
- **Sentiment Analysis**: Uses NLTK’s Vader Sentiment Analyzer to score reviews.
- **Accessibility Scoring**: Each review's sentiment score is multiplied by the presence and frequency of accessibility keywords in each category, creating a weighted rating for multiple accessibility features.
- **Aggregated Business-Level Insights**: Reviews are grouped by business, accessibility scores from each review are aggregated to create an overview of the business location's accessibilty.
- **Adjust for Review Count**: The system adjusts for review count, producing normalized scores for accurate comparison.

#### Final Accessibility Score Computation COME BACK
For each business, the final output includes:
- Overall accessibility score (sum of individual feature scores)
- Sentiment-adjusted accessibility impact
- Breakdown of accessibility feature scores per business
- Weighted recommendation ranking

### Streamlit Interface for Accessibility-Based Recommendations
This Streamlit application provides a customized accessibility search tool, allowing users to filter businesses based on their specific needs. It includes multiple accessibility-enhancing features, such as text size adjustments, high contrast mode, and text-to-speech, ensuring an inclusive experience.

### Personalized Business Recommendations
The app uses business accessibility scores to rank and suggest locations based on selected accessibility needs.
- Users select relevant accessibility categories (mobility, cognitive accessibility, sensory sensitivities, etc.)
- A weighting system allows users to prioritize certain accessibility factors.
- Businesses are sorted dynamically based on the weighted score, ensuring personalized recommendations.
- If no accessibility needs are provided, then they are sorted based on overall accessibility scores






