import asyncpg

async def create_table_messages24(connection):
    query = """
    CREATE TABLE IF NOT EXISTS messages24 (
      
      id int8 NULL,
      image text NULL,
      url text NULL,
      title text NULL,
      price text NULL,
      "size" text NULL,
      rooms text NULL,
      address text NULL,
      crawler text NULL,
      "from" text NULL,
      "to" text NULL,
      images text NULL,
      total_price text NULL,
      added_dttm text NULL
    );
    """
    await connection.execute(query)

async def create_table_last24(connection):
    query = """
    CREATE TABLE IF NOT EXISTS last_message24 (
        id serial PRIMARY KEY,
        message_id bigint,
        channel text
    );
    """
    await connection.execute(query)
    
async def insert_message(connection, id,img,url,title,prc,sz,rm,addr,crw,fr,to,imgs,totprc,add_dt):
    query = """
      INSERT INTO messages24 (
      
      id,
      image,
      url,
      title,
      price,
      "size",
      rooms,
      address,
      crawler,
      "from",
      "to",
      images,
      total_price,
      added_dttm
    ) VALUES (
      $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14);
    """
    await connection.execute(query, id,img,url,title,prc,sz,rm,addr,crw,fr,to,imgs,totprc,add_dt)

async def get_last_message_id(connection, channel):
    query = "SELECT message_id FROM last_message24 where channel=$1;"
    result = await connection.fetchval(query, channel)
    #result = await connection.execute(query, channel)
    return result if result is not None else 0

async def update_last_message_id(connection, message_id, channel):
    query = """
        UPDATE last_message24
        SET message_id = $1
        where channel = $2;
    """
    await connection.execute(query, message_id, channel)

async def init_last_message(connection, channel):
    query = """
      INSERT INTO last_message24
      (message_id, channel)
      VALUES 
      (1, $1)
    """
    await connection.execute(query, channel)