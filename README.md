# DSC-4900
# Accessibility Review Analysis
  - Start date: 01/2024
  - DSC-4900 - Data Science Project and Portfolio @ Belmont University
  - Author: Zoe Niesen

Table of Contents
---
   * [About the project](#about-the-project)
   * [Scraping data from Yelp](#scraping-data-from-yelp)
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

 
## Scraping data from Yelp
Here are the steps involved in my Yelp-Scraping Protocol

### Step 1: Initialize SQL Database

### Step 2: Get a starting link

#### a) Find a business you want to start with 
```
python scraper/scrape.py
```
