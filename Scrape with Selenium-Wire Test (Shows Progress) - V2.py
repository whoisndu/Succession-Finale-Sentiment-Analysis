# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 22:58:30 2023

@author: NDU-PC
"""

import csv
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options


def scrape_tweets():
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Create a new instance of the Chrome driver with Selenium Wire
    driver = webdriver.Chrome(options=options)
    driver.scopes = [".*twitter\.com.*"]

    # Define the hashtag to search for
    hashtag = "#successionHBO OR successionfinale"

    # Define the maximum number of tweets to scrape
    max_tweets = 1000000

    # Initialize variables
    count = 0
    tweets = []

    # Start scraping
    while count < max_tweets:
        print(f"Scraping tweets: {count}/{max_tweets}")

        # Fetch the tweets
        driver.get(f"https://twitter.com/search?q={hashtag}&f=live")

        # Wait for the page to load
        time.sleep(5)

        # Get the requests made by the browser
        requests = driver.requests

        # Extract tweet data from the requests
        for request in requests:
            if request.response:
                url = request.url
                if "https://twitter.com/i/api/graphql/" in url:
                    json_data = request.response.body.decode("utf-8")
                    # Process the JSON data and extract tweet details
                    # ...
                    # Add the tweet data to the tweets list
                    # ...
                    # Increment the count
                    # ...

        # If no more tweets are found, break the loop
        if len(tweets) == 0:
            break

        # Wait before fetching the next set of tweets
        time.sleep(180)

    # Write tweets to a CSV file if the list is not empty
    if tweets:
        with open("tweets.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=tweets[0].keys())
            writer.writeheader()
            writer.writerows(tweets)

    # Close the browser
    driver.quit()

    return count


if __name__ == "__main__":
    count = scrape_tweets()
    print(f"Total tweets scraped: {count}")
