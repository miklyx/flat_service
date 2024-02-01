from database_service import get_from_redis, init_redis
import json

def remove_backslashes(data):
  return data.replace("\\", "")

async def get_flats():
  redis = await init_redis()
  sorted_set_key = "flats_sorted_set"
  try:
      res = await get_from_redis(redis, sorted_set_key)
      #print(res)
      #data = res.decode('utf-8')
      data = json.dumps(res)
      #cleaner = remove_backslashes(data)
      #print(json.loads(data))
      #print(data.replace("\\u00",""))
      result = json.loads(data)
      #print(result)
      #result = map(lambda el: el.replace('\',''), data)
      #print(result)
      return result
  except Exception as e:
      print(f'Error: {e}')