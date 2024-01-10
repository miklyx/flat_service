import asyncio
import os
import redis
import json
from dotenv import load_dotenv

from database import asyncpg, create_table_messages24, create_table_last24, insert_message, update_last_message_id, get_last_message_id, init_last_message 

load_dotenv()

DATABASE_URL = os.environ.get('PY_DATABASE_URL')
REDIS_PWD = os.environ.get('REDIS_PWD')
REDIS_HOST = os.environ.get('REDIS_HOST')
CHANNEL_USERNAME = os.environ.get('PY_CHANNEL_USERNAME')
EXTRA_CHANNEL_USERNAME = os.environ.get('PY_CHANNEL_USERNAME_EXTRA')

async def insert_into_postgres(db_connection, flat):
    print(flat)
    print(flat.message_id)
    await insert_message(
                        db_connection, 
                        flat.message_id,
                        '',
                        flat.url,
                        flat.about,
                        flat.price,
                        flat.size,
                        '',
                        flat.address,
                        flat.channel_name,
                        '',
                        '',
                        '',
                        '',
                        flat.added_dttm
                        )

async def insert_into_redis(redis, list, flat):
    redis.sadd(list, json.dumps(flat))
    if len(redis.smembers(list)) > 20:
      redis.srem(list, redis.spop(list))

async def insert_into_redis_sorted(redis, sorted_set_key, flat):
    print(sorted_set_key)
    print(flat)
    redis.zadd(sorted_set_key, {json.dumps(flat):flat['message_id']})
    if len(redis.zrange(sorted_set_key, 0, -1)) > 40:
      oldest_element = redis.zrange(sorted_set_key, 0, 0, withscores=True)
      redis.zrem(sorted_set_key, oldest_element[0][0])

async def init_pg():
    db_connection = await asyncpg.connect(DATABASE_URL)
   
    try:
        print('creating tables')
        await create_table_messages24(db_connection)
        await create_table_last24(db_connection)
        print('populating tables')
        await init_last_message(db_connection, CHANNEL_USERNAME)
        await init_last_message(db_connection, EXTRA_CHANNEL_USERNAME)
        return db_connection
    except Exception as e:
        print(f'Error: {e}')
    
async def init_redis():
    redis_connection = redis.Redis(
      host=REDIS_HOST,
      port=15432,
      password=REDIS_PWD)
    return redis_connection