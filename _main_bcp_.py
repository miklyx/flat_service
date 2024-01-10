import asyncio
import os
import redis
import json
from dotenv import load_dotenv

from telethon import TelegramClient, functions, types
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession
from database import asyncpg, create_table_messages24, create_table_last24, insert_message, update_last_message_id, get_last_message_id, init_last_message 

load_dotenv()

API_ID = os.environ.get('PY_API_ID')
API_HASH = os.environ.get('PY_API_HASH')
PHONE_NUMBER = os.environ.get('PY_PHONE_NUMBER')
CHANNEL_USERNAME = os.environ.get('PY_CHANNEL_USERNAME')
EXTRA_CHANNEL_USERNAME = os.environ.get('PY_CHANNEL_USERNAME_EXTRA')
DATABASE_URL = os.environ.get('PY_DATABASE_URL')
PY_SESSION = os.environ.get('PY_SESSION')
REDIS_PWD = os.environ.get('REDIS_PWD')

def parse_main_bot(str):
    about = str.split('Price: ')[0]
    last = str.split('Price: ')[1]
    price = last.split('Size: ')[0]
    last = last.split('Size: ')[1]
    size = last.split('Location: ')[0]
    address_full = last.split('Location: ')[1]
    address = address_full.split('https:')[0]
    url = 'https:'+address_full.split('https:')[1]
    return [about, price, size, address, url]

def parse_extra_bot(str):
    arr = str.split('\n')
    about = arr[0]
    price = arr[3].split('Preis: ')[1]
    size = arr[2].split('Größe: ')[1]
    address_full = 'Berlin'
    address = 'Berlin'
    url = arr[5]
    return [about, price, size, address, url]

async def read_channel(client, entity, db_connection,r,list, last_message_id, channel_name, lock):
    try:
      async with lock:
        print('getting messages')
        messages = await client.get_messages(entity, limit=30)
        print('checking new')
        new_messages = [message for message in messages if message.id > last_message_id]
        if new_messages:
            last_message_id = new_messages[0].id
            for message in new_messages:
                if channel_name=='berlin_apartment_bot':
                    print('old bot')
                    print(message.raw_text.split('\n'))
                    str=message.raw_text
                    about = str.split('Price: ')[0]
                    last = str.split('Price: ')[1]
                    price = last.split('Size: ')[0]
                    last = last.split('Size: ')[1]
                    size = last.split('Location: ')[0]
                    address_full = last.split('Location: ')[1]
                    address = address_full.split('https:')[0]
                    url = 'https:'+address_full.split('https:')[1]
                    flat = {
                        "message_id":message.id,
                        "url":url,
                        "about":about,
                        "price":price,
                        "size":size,
                        "address":address,
                        "channel_name":channel_name,
                        'added_dttm':message.date.strftime("%d/%m/%Y, %H:%M:%S")
                      }
                    await insert_message(
                        db_connection, 
                        message.id,
                        '',
                        url,
                        about,
                        price,
                        size,
                        '',
                        address,
                        channel_name,
                        '',
                        '',
                        '',
                        '',
                        message.date.strftime("%d/%m/%Y, %H:%M:%S")
                        )
                    r.sadd(list, json.dumps(flat))
                    if len(r.smembers(list)) > 20:
                      r.srem(list, r.spop(list))
                else :
                    str=message.raw_text
                    data = parse_extra_bot(str)
                    print('new bot')
                    print(data)
                    await insert_message(
                        db_connection, 
                        message.id,
                        '',
                        data[4],
                        data[0],
                        data[1],
                        data[2],
                        '',
                        data[3],
                        channel_name,
                        '',
                        '',
                        '',
                        '',
                        message.date.strftime("%d/%m/%Y, %H:%M:%S")
                        )
            await update_last_message_id(db_connection, last_message_id, channel_name)
    except Exception as e:
        print(f'Error reading channel: {e}')

async def main():
    client = TelegramClient(StringSession(PY_SESSION), API_ID, API_HASH)

    db_connection = await asyncpg.connect(DATABASE_URL)
    r = redis.Redis(
      host='redis-15432.c323.us-east-1-2.ec2.cloud.redislabs.com',
      port=15432,
      password=REDIS_PWD)
    list_key = "flats"
    set_key = "flats_set"
    #r.ltrim(list_key, 0, 19)
    try:
        await client.start()
        print('creating table')
        await create_table_messages24(db_connection)
       
        await create_table_last24(db_connection)
        print('populating table ')
        await init_last_message(db_connection, CHANNEL_USERNAME)
        await init_last_message(db_connection, EXTRA_CHANNEL_USERNAME)
        print('Telegram client started')
        last_message_id = await get_last_message_id(db_connection, CHANNEL_USERNAME)
        last_message_extra_id = await get_last_message_id(db_connection, EXTRA_CHANNEL_USERNAME)
        entity = await client.get_entity(CHANNEL_USERNAME)
        entity_extra = await client.get_entity(EXTRA_CHANNEL_USERNAME)
        lock = asyncio.Lock()

        while True:
            await asyncio.gather(
                read_channel(client, entity, db_connection,r, set_key, last_message_id, CHANNEL_USERNAME, lock),
                #read_channel(client, entity_extra, db_connection, last_message_extra_id, EXTRA_CHANNEL_USERNAME, lock)
            )
            last_message_id = await get_last_message_id(db_connection, CHANNEL_USERNAME)
            last_message_extra_id = await get_last_message_id(db_connection, EXTRA_CHANNEL_USERNAME)
            await asyncio.sleep(300)

    except SessionPasswordNeededError:
        code = input('Please enter the two-factor authentication code from your Telegram app: ')
        await client(functions.auth.CheckPasswordRequest(code=code))
    except Exception as e:
        print(f'Error: {e}')
    finally:
        await client.disconnect()
        await db_connection.close()


if __name__ == '__main__':
    asyncio.run(main())

