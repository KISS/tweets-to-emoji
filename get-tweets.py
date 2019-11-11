import os
import tweepy as tw
import pandas as pd
import datetime
import time

consumer_key = 'xxx'
consumer_secret = 'xxx'
access_token = 'xxx'
access_token_secret = 'xxx'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def request_data(search_params, lang, term):
  # collect tweets
  source_tweets = tw.Cursor(api.search, q=search_params, lang=lang, result_type="mixed").items(100)

  # store filtered tweets
  cleaned_tweets = []

  # iterate and filter out data from collected tweets
  for tweet in source_tweets:
    tweet = tweet._json

    # filter for data we care about
    data = {}
    data['timestamp'] = tweet['created_at']
    data['id'] = tweet['id']
    data['text'] = tweet['text']
    data['truncated'] = tweet['truncated']
    data['hashtags'] = tweet['entities']['hashtags']
    data['symbols'] = tweet['entities']['symbols']
    data['result_type'] = tweet['metadata']['result_type']
    data['retweet_count'] = tweet['retweet_count']
    data['favorite_count'] = tweet['favorite_count']
    data['possibly_sensitive_link'] = tweet['possibly_sensitive'] if 'possibly_sensitive' in tweet else None
    data['lang'] = tweet['lang']
    data['user_handle'] = tweet['user']['screen_name']
    data['user_name'] = tweet['user']['name']
    data['user_follower_count'] = tweet['user']['followers_count']
    data['user_favorites_count'] = tweet['user']['favourites_count']
    data['user_lifetime_interactions'] = tweet['user']['statuses_count']

    # log term searched for
    data['filtered_for'] = term
    cleaned_tweets.append(data)

  df_data = [[tweet['timestamp'], tweet['id'], tweet['text'], tweet['truncated'], tweet['hashtags'], tweet['symbols'], tweet['retweet_count'], tweet['favorite_count'], tweet['possibly_sensitive_link'], tweet['lang'], tweet['result_type'], tweet['filtered_for'], tweet['user_handle'], tweet['user_name'], tweet['user_follower_count'], tweet['user_favorites_count'], tweet['user_lifetime_interactions']] for tweet in cleaned_tweets]

  df_fields = ['timestamp', 'id', 'text', 'truncated', 'hashtags', 'symbols', 'retweet_count', 'favorite_count', 'possibly_sensitive_link', 'lang', 'result_type', 'filtered_for', 'user_handle', 'user_name', 'user_follower_count', 'user_favorites_count', 'user_lifetime_interactions']

  df = pd.DataFrame(data=df_data, columns=df_fields)

  # get current timestamp
  timestamp = str(datetime.datetime.now())

  # save to json
  df.to_json(r'/Users/luisamarieth/projects/tweet-to-emoji/json/tweets_' + term + '_' + timestamp + '.json', orient='records')

  # save to csv
  df.to_csv(r'/Users/luisamarieth/projects/tweet-to-emoji/csv/tweets_' + term + '_' + timestamp + '.csv', index = None, header=True)

# define the search terms and lang
lang = 'en'
fixed_filters = '-filter:retweets -filter:mentions -filter:replies -filter:media'
words_to_filter_for = ['sad', 'depressed', 'angry', 'rage', 'happy', 'glad', 'scared', 'afraid', 'nervous', 'surprised', 'love', 'disgusting', 'gross', 'excited', 'hate', 'thankful', 'lit', 'disappointed', 'upset', 'grateful']
# negate all terms filtered for to retrieve tweets that don't contain any of those words
words_to_filter_out = ' -'.join(words_to_filter_for)

# make a single request to the API
def single_request():
    # request tweets for each custom search terms
    for word in words_to_filter_for:
      search_params = word + ' ' + fixed_filters
      request_data(search_params, lang, word)

    # request tweets that don't contain any of the custom search terms
    search_params = '-' + words_to_filter_out + ' ' + fixed_filters
    request_data(search_params, lang, "none")

# single_request()

# make a request to the API every x-seconds
def recurring_request(requests_to_make, timeout):
  requests_made = 0

  while requests_made < requests_to_make:
    # request tweets for each custom search terms
    for word in words_to_filter_for:
      search_params = word + ' ' + fixed_filters
      request_data(search_params, lang, word)

    # request tweets that don't contain any of the custom search terms
    search_params = '-' + words_to_filter_out + ' ' + fixed_filters
    request_data(search_params, lang, "none")

    requests_made += 1
    time.sleep(timeout)

requests_to_make = 1
timeout = 15 * 60
# recurring_request(requests_to_make, timeout)