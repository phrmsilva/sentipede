import json
from requests_oauthlib import OAuth1
from twitter_tokens import *
import requests
import sys
import unicodedata
""" How to use:
    Provide file access_tokens.py with:
      consumer_key, consumer_secret,
      access_key, and access_secret defined.
    
    Request_tweets:
    Inputs:
    - query: String to search for 
    - count: Int how many tweets to search for 
    - date: String in the format 'YYYY-MM-DD'

    Returns:
    List of String with tweets
    len(result) = count
"""



def request_tweets(query, count, date): 

  auth = OAuth1(consumer_key, consumer_secret,
                  access_key, access_secret)
  search_url = 'https://api.twitter.com/1.1/search/tweets.json'

  req_tweets = requests.get(search_url, auth=auth, 
    params={'q': query, 'lang': 'en', 'count': count, 'until' : date})

  ######################################
  ## JSON PARSING
  json_data = json.loads(req_tweets.content)

  statuses = json_data["statuses"]

  all_tweets = []
  for tweet in statuses:
    all_tweets.append(unicodedata.normalize('NFKD', tweet["text"]).encode('ascii','ignore'))

  return all_tweets