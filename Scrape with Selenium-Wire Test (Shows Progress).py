# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 22:38:35 2023

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

        # Extract tweet elements
        tweet_elements = driver.find_elements_by_css_selector(
            'div[data-testid="tweet"]'
        )

        # Process each tweet element
        for element in tweet_elements:
            # Extract tweet details
            tweet_data = {
                "date": element.get_attribute("data-time"),
                "url": element.get_attribute("href"),
                "content": element.find_element_by_css_selector(
                    'div[data-testid="tweet"] div[lang]'
                ).text,
                "renderedContent": element.find_element_by_css_selector(
                    'div[data-testid="tweet"] div[lang]'
                ).get_attribute("innerHTML"),
                "id": element.get_attribute("data-tweet-id"),
                "user.username": element.find_element_by_css_selector(
                    ".css-901oao.css-bfa6kz.r-1qd0xha.r-n6v787.r-16dba41.r-1cwl3u0.r-bcqeeo.r-qvutc0"
                )
                .get_attribute("href")
                .split("/")[-1],
                "user.displayname": element.find_element_by_css_selector(
                    ".css-901oao.css-bfa6kz.r-n6v787.r-1qd0xha.r-16dba41.r-bcqeeo.r-bnwqim.r-qvutc0"
                ).text,
                "user.id": element.find_element_by_css_selector(
                    ".css-901oao.css-bfa6kz.r-n6v787.r-1qd0xha.r-16dba41.r-bcqeeo.r-qvutc0"
                )
                .get_attribute("href")
                .split("/")[-1],
                "user.description": element.find_element_by_css_selector(
                    ".css-901oao.css-bfa6kz.r-n6v787.r-1qd0xha.r-16dba41.r-bcqeeo.r-bnwqim.r-qvutc0+div"
                ).text,
                "user.verified": bool(
                    element.find_elements_by_css_selector(
                        ".css-4rbku5.css-18t94o4.css-901oao.r-1fmj7o5.r-1qd0xha.r-n6v787.r-bcqeeo.r-qvutc0"
                    )
                ),
                "user.created": element.find_element_by_css_selector(
                    'div[data-testid="tweet"] a[role="link"]'
                ).get_attribute("title"),
                "user.followersCount": element.find_element_by_css_selector(
                    'div[data-testid="tweet"] div[dir="ltr"]'
                ).text,
                "user.friendsCount": element.find_element_by_css_selector(
                    'div[data-testid="tweet"] div[dir="ltr"]+div'
                ).text,
                "user.statusesCount": element.find_element_by_css_selector(
                    'div[data-testid="tweet"] div[dir="ltr"]+div+div'
                ).text,
            }

            tweets.append(tweet_data)

        count += len(tweet_elements)

        # If no more tweets are found, break the loop
        if len(tweet_elements) == 0:
            break

        # Wait before fetching the next set of tweets
        time.sleep(180)

    # Write tweets to a CSV file
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
