# Sentiments are coming from the JSON file.
# Values are coming from the CSV files.
import json
from stockprice import gen_interface
#from main import correlation

## CONSTANTS
dates = []

for i in range(2, 7):
  dates.append('2015-02-0' + str(i))

companies_names = ['apple', 'berkshire hathaway', 'facebook',
   'general electric', 'google', 'hubspot', 'nestle', 'novartis', 
   'trip advisor']
companies_codes = ['AAPL', 'BRK.A', 'FB', 'GE', 'GOOG', 'HUBS', 'NSRGY', 
   'NVS', 'TRIP']

## READ SENTIMENT DATA

with open('sentdata.json') as json_data:
  sentiments = json.load(json_data)

## READ PRICES DATA
values = {}

for co in companies_codes:
  values[co] = {}
  for d in dates:
    openf = gen_interface('Open', co, d)
    close = gen_interface('Close', co, d)
    values[co][d] = ((close - openf) * 100.0) / openf

print '\n'
for i in range(0, len(companies_codes)):
  print companies_names[i] + ' - ' + companies_codes[i] + '\n'
  for d in dates:
    print d
    print 'Price change: %.2f%%' % (values[companies_codes[i]][d])
    print 'Positive tweets: %.2f%%\n' % (sentiments[companies_codes[i]][d]['pos'] * 100)
  print '-' * 20

