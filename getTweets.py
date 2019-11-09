import os
import tweepy as tw
import pandas as pd

consumer_key= 'xxx'
consumer_secret= 'xxx'
access_token= 'xxx'
access_token_secret= 'xxx'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and lang
lang = "en"
fixed_filters = "-filter:retweets -filter:mentions -filter:replies -filter:media"
custom_search_term = "sad"
search_params = custom_search_term + " " + fixed_filters

print(search_params)

# Collect tweets
tweets = tw.Cursor(api.search, q=search_params, lang=lang).items(2)

# Iterate and print tweets
for tweet in tweets:
  tweet = tweet._json

  # data we care about
  tweet_timestamp = tweet['created_at']
  tweet_id = tweet['id']
  text = tweet['text']
  truncated = tweet['truncated']
  hashtags = tweet['entities']['hashtags']
  symbols = tweet['entities']['symbols']
  metadata = tweet['metadata']
  user_screen_name = tweet['user']['screen_name']
  user_name = tweet['user']['name']
  user_follower_count = tweet['user']['followers_count']
  user_favorites_count = tweet['user']['favourites_count']
  lifetime_interactions = tweet['user']['statuses_count']
  tweet_retweet_count = tweet['retweet_count']
  tweet_favorite_count = tweet['favorite_count']
  possibly_sensitive_link = tweet['possibly_sensitive'] if "possibly_sensitive" in tweet else None
  lang = tweet['lang']

  # create dataframe
  Tweet = {
    'tweet_timestamp': [tweet_timestamp],
    'tweet_id': [tweet_id],
    'text': [text]
  }

  df = pd.DataFrame(Tweet, columns = ['tweet_timestamp', 'tweet_id', 'text'])
  print(df)

  # save in json file
  df.to_json(r'/Users/luisamarieth/projects/tweet-to-emoji/tweet2.json')

  # save in csv
  df.to_csv (r'/Users/luisamarieth/projects/tweet-to-emoji/tweet.csv', index = None, header=True)

  # with open('tweet.csv', 'a') as f:
  #   df.to_csv(f, header=False)

  # print(tweet_timestamp, tweet_id, text, truncated, hashtags, symbols, metadata, user_screen_name, user_name, user_follower_count, user_favorites_count, lifetime_interactions, tweet_retweet_count, tweet_favorite_count, possibly_sensitive_link, lang)