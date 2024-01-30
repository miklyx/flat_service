from database_service import get_from_redis, init_redis
import json

async def get_flats():
  redis = await init_redis()
  sorted_set_key = "flats_sorted_set"
  try:
      res = await get_from_redis(redis, sorted_set_key)
      #print(res)
      #data = res.decode('utf-8')
      data = json.dumps(res)
      print(data.replace("\\u00",""))
      return data
  except Exception as e:
      print(f'Error: {e}')