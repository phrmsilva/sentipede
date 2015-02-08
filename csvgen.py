import sys
import json
import requests
import csv
from twitter_search import request_tweets
from sentiments import analyse
from stockprice import gen_interface
# Generates the CSV file of the sentiments of a given word
# over Feb, 2nd - 6th, 2015

## SEARCH PARAMETERS

count = 100
d = '2015-02-0'
days_list = range(2, 7) #  INVARIANT: len(days_list) is 5
date_pos, date_neg, date_neutral = [], [], []

def generateWeek(word):
  # Fill sentiment for date's lists
  for i in days_list:
    date = d + str(i)

    tweets = request_tweets(word, count, date)
    query = compress(tweets)
    sentiment = analyse(query)

    pos = sentiment['pos'] # 0 <= pos <= 1
    # save results for later csv file
    date_pos.append(pos)
    date_neg.append(sentiment['neg'])
    date_neutral.append(sentiment['neutral'])

  with open(word + '.csv', 'w') as csvfile:
    fieldnames = ['date', 'pos', 'neg', 'neutral']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(0, 5):
      date = d + str(i + 2)
      writer.writerow({'date': date, 'pos': date_pos[i],
       'neg': date_neg[i], 'neutral': date_neg[i]})


def compress(strs):
  r = ''
  for s in strs:
    r += s
  return r
