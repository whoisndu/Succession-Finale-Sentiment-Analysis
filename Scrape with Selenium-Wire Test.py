from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv


def scrape_tweets():
    hashtag1 = "#successionHBO"
    hashtag2 = "successionfinale"
    count = 0
    max_tweets = 1000000

    # Configure Selenium Wire with user agent of an older version of Chrome
    options = Options()
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    )
    driver = webdriver.Chrome(seleniumwire_options={"options": options})

    # Scrape tweets with the specified hashtags until the maximum limit is reached
    tweets = []
    driver.get(
        f"https://twitter.com/search?q={hashtag1}%20OR%20{hashtag2}&src=typed_query"
    )

    while count < max_tweets:
        # Scroll down to load more tweets
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(3)  # Adjust the delay as needed

        # Find and extract tweet elements
        tweet_elements = driver.find_elements(
            By.XPATH, '//div[@data-testid="tweet"]'
        )
        for tweet_element in tweet_elements:
            count += 1
            tweet_data = {
                "date": tweet_element.get_attribute(
                    "data-time"
                ),  # Date and time
                "url": tweet_element.find_element(
                    By.XPATH, './/a[starts-with(@href, "/")]'
                ).get_attribute(
                    "href"
                ),  # URL
                "content": tweet_element.find_element(
                    By.XPATH, './/div[@data-testid="tweet"]'
                ).text,  # Content
                "renderedContent": tweet_element.get_attribute(
                    "innerHTML"
                ),  # Rendered Content
                "id": tweet_element.get_attribute("data-tweet-id"),  # ID
                "user.username": tweet_element.find_element(
                    By.XPATH, './/a[starts-with(@href, "/")]/div/div[2]'
                ).text,  # Username
                "user.displayname": tweet_element.find_element(
                    By.XPATH, './/div[@data-testid="tweet"]'
                ).get_attribute(
                    "data-name"
                ),  # Display Name
                "user.id": tweet_element.find_element(
                    By.XPATH, './/a[starts-with(@href, "/")]'
                ).get_attribute(
                    "data-user-id"
                ),  # User ID
                "user.description": tweet_element.find_element(
                    By.XPATH, './/a[starts-with(@href, "/")]/div/div[4]'
                ).text,  # User Description
                "user.verified": tweet_element.get_attribute(
                    "data-verified"
                ),  # User Verification
                "user.created": tweet_element.get_attribute(
                    "data-user-created"
                ),  # User Account Creation Date
                "user.followersCount": tweet_element.get_attribute(
                    "data-followers-count"
                ),  # User Followers Count
                "user.friendsCount": tweet_element.get_attribute(
                    "data-friends-count"
                ),  # User Friends Count
                "user.statusesCount": tweet_element.get_attribute(
                    "data-statuses-count"
                ),  # User Total Tweets Count
                "user.location": tweet_element.find_element(
                    By.XPATH, './/a[starts-with(@href, "/")]/div/div[3]'
                ).text,  # User Location
                "user.descriptionUrls": tweet_element.find_element(
                    By.XPATH, './/a[starts-with(@href, "/")]/div/div[4]'
                ).get_attribute(
                    "hrefs"
                ),  # User Description URLs
                "user.linkUrl": tweet_element.find_element(
                    By.XPATH, './/a[starts-with(@href, "/")]/div/div[2]'
                ).get_attribute(
                    "href"
                ),  # User Profile URL
                # ... Add more attributes as needed
            }
            tweets.append(tweet_data)
            print(f'Tweet #{count}: {tweet_data["content"]}')

            if count >= max_tweets:
                break

    # Save tweets to a CSV file
    filename = r"C:\Users\NDU-PC\Desktop\tweets.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=tweets[0].keys())
        writer.writeheader()
        writer.writerows(tweets)

    driver.quit()
    return count


def main():
    while True:
        count = scrape_tweets()
        print(f"Total tweets scraped: {count}")

        if count >= 1000000:
            print("Maximum limit reached. Exiting the script.")
            break

        time.sleep(600)  # Sleep for 10 minutes

        print("Sleeping for 3 minutes...")
        time.sleep(180)  # Sleep for 3 minutes


if __name__ == "__main__":
    main()
