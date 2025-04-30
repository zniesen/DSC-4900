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
The data used for this project was a combination of data I scraped prior to Yelp's security escalation, data I scraped manually, the Yelp API, and multiple public Kaggle datasets _**(COME BACK)**_
-

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

## Scraping data from Yelp



