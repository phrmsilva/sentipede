import requests
import pandas as pd


def INTERNAL_makeURLfromParams(start_date,end_date,ticker_symbol):
    INTERNAL_base = 'http://ichart.finance.yahoo.com/table.csv'
    INTERNAL_startstr = start_date.split('-')
    INTERNAL_endstr = end_date.split('-')
    payload = {'s' : ticker_symbol,'a' :INTERNAL_startstr[0] ,'b':INTERNAL_startstr[1],'c':INTERNAL_startstr[2],'d':INTERNAL_endstr[0],'e':INTERNAL_endstr[1],'f':INTERNAL_endstr[2],'g':'d','ignore':'.csv'}
    return requests.get(INTERNAL_base,params=payload)

def INTERNALwritebackread(startdate,enddate,symbol):
    retcsv = INTERNAL_makeURLfromParams(startdate,enddate,symbol)
    with open(startdate+enddate+symbol+'.csv','wb') as fd:
        for chunk in retcsv.iter_content(chunk_size=256):
            fd.write(chunk)
    frameback = pd.read_csv(startdate+enddate+symbol+'.csv')
    return frameback


###USE THIS

def simplePullByDate(date,symbol):
    retframe = INTERNALwritebackread(date,date,symbol)
    return retframe['Adj Close']
