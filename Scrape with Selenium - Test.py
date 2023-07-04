from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv

def scrape_tweets():
    hashtag1 = "#successionHBO"
    hashtag2 = "successionfinale"
    count = 0
    max_tweets = 1000000
    
    # Configure Selenium with user agent of an older version of Chrome
    options = Options()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    
    # Scrape tweets with the specified hashtags until the maximum limit is reached
    tweets = []
    driver.get(f"https://twitter.com/search?q={hashtag1}%20OR%20{hashtag2}&src=typed_query")
    
    while count < max_tweets:
        # Scroll down to load more tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Adjust the delay as needed
        
        # Find and extract tweet elements
        tweet_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweet"]')
        for tweet_element in tweet_elements:
            count += 1
            tweet_data = [
                tweet_element.get_attribute('data-time'),  # Date and time
                tweet_element.find_element(By.XPATH, './/a[starts-with(@href, "/")]').get_attribute('href'),  # URL
                tweet_element.find_element(By.XPATH, './/div[@data-testid="tweet"]').text,  # Content
                tweet_element.get_attribute('innerHTML'),  # Rendered Content
                tweet_element.get_attribute('data-tweet-id'),  # ID
                # ... Add more attributes as needed
            ]
            tweets.append(tweet_data)
            print(f'Tweet #{count}: {tweet_data[2]}')
            
            if count >= max_tweets:
                break
        
    # Save tweets to a CSV file
    filename = r'C:\Users\Desktop\tweets.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Date', 'URL', 'Content', 'Rendered Content', 'ID', ...
        ])
        writer.writerows(tweets)
        
    driver.quit()
    return count

def main():
    while True:
        count = scrape_tweets()
        print(f'Total tweets scraped: {count}')
        
        if count >= 1000000:
            print('Maximum limit reached. Exiting the script.')
            break
        
        time.sleep(600)  # Sleep for 10 minutes
        
        print('Sleeping for 3 minutes...')
        time.sleep(180)  # Sleep for 3 minutes

if __name__ == '__main__':
    main()

