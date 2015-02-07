import requests
import xml.etree.ElementTree as ET

url = 'http://dev.markitondemand.com/Api/v2/Quote'


def request_stock(code):
  req_stock = requests.get(url, params={'symbol': code})

  tree = ET.fromstring(req_stock.content)
  root = {}

  for child in tree:
      root[child.tag.split("}")[0]] = child.text

  change = root["ChangePercent"]
  price = root['LastPrice']

  return {'price': price, 'change' : change }



request_stock('GE')