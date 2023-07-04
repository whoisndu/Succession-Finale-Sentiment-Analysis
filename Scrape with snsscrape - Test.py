import snscrape.modules.twitter as sntwitter
import csv
import time

def scrape_tweets():
    hashtag1 = "#successionHBO"
    hashtag2 = "successionfinale"
    count = 0
    max_tweets = 1000000
    
    # Scrape tweets with the specified hashtags until the maximum limit is reached
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(f'{hashtag1} OR {hashtag2}').get_items():
        count += 1
        tweet_data = [
            tweet.date, tweet.url, tweet.content, tweet.renderedContent, tweet.id,
            tweet.user.username, tweet.user.displayname, tweet.user.id, tweet.user.description,
            tweet.user.verified, tweet.user.created, tweet.user.followersCount, tweet.user.friendsCount,
            tweet.user.statusesCount, tweet.user.location, tweet.user.descriptionUrls, tweet.user.linkUrl,
            tweet.user.profileImageUrl, tweet.user.profileBannerUrl, tweet.replyCount, tweet.retweetCount,
            tweet.likeCount, tweet.quoteCount, tweet.lang, tweet.source, tweet.retweetedTweet,
            tweet.quotedTweet, tweet.mentionedUsers, tweet.hashtags
        ]
        tweets.append(tweet_data)
        print(f'Tweet #{count}: {tweet.content}')
        
        if count >= max_tweets:
            break
        
    # Save tweets to a CSV file
    filename = r'C:\Users\NDU-PC\Desktop\tweets.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Date', 'URL', 'Content', 'Rendered Content', 'ID', 'Username', 'Display Name',
            'User ID', 'User Description', 'Verified', 'User Created', 'Followers Count',
            'Friends Count', 'Statuses Count', 'User Location', 'User Description URLs',
            'User Link URL', 'User Profile Image URL', 'User Profile Banner URL', 'Reply Count',
            'Retweet Count', 'Like Count', 'Quote Count', 'Language', 'Source', 'Retweeted Tweet',
            'Quoted Tweet', 'Mentioned Users', 'Hashtags'
        ])
        writer.writerows(tweets)
        
    return count

def main():
    while True:
        count = scrape_tweets()
        print(f'Total tweets scraped: {count}')
        
        # Check if the maximum limit has been reached
        if count >= 1000000:
            print('Maximum limit reached. Exiting the script.')
            break
        
        # Sleep for 10 minutes
        time.sleep(600)
        
        # Sleep for 3 minutes
        print('Sleeping for 3 minutes...')
        time.sleep(180)

if __name__ == '__main__':
    main()

