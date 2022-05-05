import requests
from requests.adapters import HTTPAdapter
from math import ceil
import json
import time

BASE_API = 'https://shopee.vn'
NUM_COMMENT_PER_BATCH =  50

adapter = HTTPAdapter(max_retries=3)
session = requests.Session()
session.mount(BASE_API, adapter)

def error(func):
    def handlingError(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            print("Sleep for 60 seconds and invoke again")
            time.sleep(60)
            try:
                return func(*args, **kwargs)
            except Exception as e:    
                print(e)
        except Exception as e:
            print(e)
    return handlingError

@error
def get(url, data=None, headers=None, auth=None):
  response = session.get(f'{BASE_API}{url}',params=data,headers=headers, auth=auth)
  print(f"GET ROUTER {response.request.url}")
  response.raise_for_status()
  return response

def getApiComment(itemid, shopid, offset=0, limit=NUM_COMMENT_PER_BATCH):
  url = f'/api/v2/item/get_ratings?filter=1&flag=1&itemid={itemid}&limit={limit}&offset={offset}&shopid={shopid}'
  headers = {}
  return url, headers

@error
def getBatchComment(itemid, shopid, offset=0, limit=NUM_COMMENT_PER_BATCH):
  url, headers = getApiComment(itemid, shopid, offset, limit)
  response = get(url, headers=headers)
  data = json.loads(response.text)['data']['ratings']
  data = map(lambda x: dict(commentId=x['orderid'],comment=x['comment'],rating=x['rating_star']), data)
  return data

@error
def getSummaryRating(itemid, shopid):
  url, headers = getApiComment(itemid, shopid, 0, 1)
  response = get(url, headers=headers)
  data = json.loads(response.text)['data']['item_rating_summary']
  return data

def getComments(itemid, shopid, reviewCount):
  comments = []
  page_num = ceil(float(reviewCount) / NUM_COMMENT_PER_BATCH)
  limit = NUM_COMMENT_PER_BATCH
  for page in range(0, page_num):
    if page == int(page_num) - 1:
      limit = reviewCount - page*NUM_COMMENT_PER_BATCH
    comments += getBatchComment(itemid, shopid, page*NUM_COMMENT_PER_BATCH, limit)
    # For product with more than 1000 comments
    if len(comments) >= 1000:
      break
  return comments[:1000]

class ShopeeCrawler:
  @staticmethod
  def getComments(itemid, shopid):
    summaryRating = getSummaryRating(itemid, shopid)
    comments = getComments(itemid, shopid, summaryRating['rcount_with_context'])
    isEntire = (summaryRating['rcount_with_context'] <= 1000)
    return comments, isEntire
