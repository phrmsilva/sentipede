import requests
import json

#########################################
## ANALYSIS PARAMETERS

post_url = 'http://text-processing.com/api/sentiment/'

data_text = 'text=' 

def analyse(str):
  post = requests.post(url=post_url, data='text=' + str)

  ## JSON PARSING 
  pjson_data = json.loads(post.content)

  pos = pjson_data['probability']['pos']
  neg = pjson_data['probability']['neg']
  neutral = pjson_data['probability']['neutral']
  
  return {'pos': pos, 'neg': neg, 'neutral': neutral}