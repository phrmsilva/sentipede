import sys
import json
import requests
import csv
from math import sqrt
from twitter_search import request_tweets
from sentiments import analyse
from stockprice import gen_interface
from csvgen import generateWeek

## SEARCH PARAMETERS
count = 100
date = '2015-02-02' 
companies_names = ['apple', 'berkshire hathaway', 'facebook',
   'general electric', 'google', 'hubspot', 'nestle', 'novartis', 
   'tripadvisor']
companies_codes = ['AAPL', 'BRK.A', 'FB', 'GE', 'GOOG', 'HUBS', 'NSRGY', 
   'NVS', 'TRIP']
companies_pos, companies_neg, companies_neutral = [], [], []

fullsearch = {}

def all_dates():
  result = []
  for i in range(2, 7):
    result.append('2015-02-0' + str(i))
  return result

# List of String -> String
# Concatenates all the string in the given list
def compress(strings):
  result = ''
  for s in strings:
    result += s
  return result


## SEARCH LOOP
def loopSearch(date='2015-02-06'):
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
    print "Positive feeling was %.2f %% (%.2f%%)" % (pos * 100,  pos * 100 - 50)

    # calculating price change
    opening = gen_interface('Open', companies_codes[i], date)
    closing = gen_interface('Close', companies_codes[i], date)
    dif = closing - opening

    difpc = (dif * 100.0) / opening
    print "Change in value on %s was %f %%" % (date, difpc)
    print '-' * 9

def sentimentsOnDate(date):
  loopSearch()
  with open('sentipedes.csv', 'w') as csvfile:
      fieldnames = ['date', 'company_code', 'pos', 'neg', 'neutral']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      writer.writeheader()
      for i in range(0, len(companies_codes)):
        writer.writerow({'date': date, 'company_code': companies_codes[i],
         'pos': companies_pos[i], 'neg': companies_neg[i],
         'neutral':companies_neutral[i]})

def sentimentsByCompany(company_name):
  generateWeek(company_name)

def plot():
  dofullsearch();
  json_str = json.dumps(fullsearch)
  # Writing JSON data
  with open('sentdata.json', 'w') as f:
    json.dump(fullsearch, f, indent=2, separators=(',', ': '))

def dofullsearch():
  for c in companies_codes:
    fullsearch[c] = {}
    for d in all_dates():
      fullsearch[c][d] = analyse(compress(request_tweets(c, count, d)))

# Calculates the covalence of the price changes and positive tweets on a
# company
def covalence(list_difc, list_pos):
  ave_change = average(list_difc)
  ave_sense = average(list_pos)
  total = 0

  for i in range(0, 5):
    total += ((list_difc[i] - ave_change) * (list_pos[i] - ave_sense))

  return total/4.0

def average(list_of_number):
  return (sum(list_of_number)/len(list_of_number))


def correlation(list_difc, list_pos):
  cov = covalence(list_difpc, list_pos)
  ssense = helper(list_pos)
  schange = helper(list_difc)

  return (cov(list_difc, list_pos) / ( ssense * schange ))

def helper(list_of_number):
  ave = average(list_of_number)
  total = 0
  for n in list_of_number:
    total += (n - ave)**2
  return sqrt(total/len(list_of_number))

#loopSearch()
#plot()
