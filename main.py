import sys
import json
import requests
import csv
from twitter_search import request_tweets
from sentiments import analyse
from stockprice import gen_interface


# List of String -> String
# Concatenates all the string in the given list
def compress(strings):
  result = ''
  for s in strings:
    result += s
  return result


## SEARCH PARAMETERS

count = 100
date = '2015-02-06' 
companies_names = ['berkshire hathaway', 'google', 'general electric', 
  'facebook', 'apple']
companies_codes = ['BRK.A', 'GOOG', 'GE', 'FB', 'AAPL']
companies_pos, companies_neg, companies_neutral = [], [], []

## SEARCH LOOP

for i in range(0, len(companies_names)):

  # get tweets
  tweets = request_tweets(companies_names[i], count, date)
  query = compress(tweets)

  # analyse tweets
  sentiment = analyse(query)
  pos = sentiment['pos'] # 0 <= pos <= 1
  # save results for later csv file
  companies_pos.append(pos)
  companies_neg.append(sentiment['neg'])
  companies_neutral.append(sentiment['neutral'])

  print companies_names[i]
  print "Positive feeling was %.2f %%" % (pos * 100)

  # calculating price change
  opening = gen_interface('Open', companies_codes[i], date)
  closing = gen_interface('Close', companies_codes[i], date)
  dif = opening - closing

  print "Change in value on %s was %d" % (date, dif)
  print '-' * 9

with open('sentipedes.csv', 'w') as csvfile:
    fieldnames = ['date', 'company_code', 'pos', 'neg', 'neutral']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(0, len(companies_codes)):
      writer.writerow({'date': date, 'company_code': companies_codes[i],
       'pos': companies_pos[i], 'neg': companies_neg[i],
       'neutral':companies_neutral[i]})

