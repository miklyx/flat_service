import asyncio
import os
#import redis
#import json
from dotenv import load_dotenv

#from telethon import TelegramClient, functions, types
#from telethon.errors import SessionPasswordNeededError
#from telethon.sessions import StringSession

from database import asyncpg, create_table_messages24, create_table_last24, insert_message, update_last_message_id, get_last_message_id, init_last_message 
from database_service import insert_into_postgres, insert_into_redis, init_pg, init_redis, insert_into_redis_sorted

from telegram_client import telegram_client
from telegram_service import read_channel

load_dotenv()

#API_ID = os.environ.get('PY_API_ID')
#API_HASH = os.environ.get('PY_API_HASH')
#PHONE_NUMBER = os.environ.get('PY_PHONE_NUMBER')
CHANNEL_USERNAME = os.environ.get('PY_CHANNEL_USERNAME')
#EXTRA_CHANNEL_USERNAME = os.environ.get('PY_CHANNEL_USERNAME_EXTRA')
#DATABASE_URL = os.environ.get('PY_DATABASE_URL')
#PY_SESSION = os.environ.get('PY_SESSION')
#REDIS_PWD = os.environ.get('REDIS_PWD')



async def main():
    client = await telegram_client()
    #db_connection = await init_pg()
    r = await init_redis()
    set_key = "flats_set"
    sorted_set_key = "flats_sorted_set"
    try:
        #last_message_id = await get_last_message_id(db_connection, CHANNEL_USERNAME)
        #last_message_extra_id = await get_last_message_id(db_connection, EXTRA_CHANNEL_USERNAME)
        #entity = await client.get_entity(CHANNEL_USERNAME)
        #entity_extra = await client.get_entity(EXTRA_CHANNEL_USERNAME)
        lock = asyncio.Lock()
        while True:
            flats = await read_channel(client, 0, CHANNEL_USERNAME, lock)
            #for flat in flats:
            #  print(flat)
            for flat in flats:
              #await insert_into_postgres(db_connection, flat)
              #print('before redis')
              await insert_into_redis_sorted(r, sorted_set_key, flat)

            #await insert_into_redis(r, set_key, flat)
            #last_message_id = await get_last_message_id(db_connection, CHANNEL_USERNAME)
            #last_message_extra_id = await get_last_message_id(db_connection, EXTRA_CHANNEL_USERNAME)
            await asyncio.sleep(300)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    asyncio.run(main())

