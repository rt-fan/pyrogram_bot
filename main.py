from sqlalchemy import create_engine, Table, Column, Integer, BigInteger, String, DateTime, MetaData
from datetime import datetime
import pathlib
from asyncio import sleep
from configparser import ConfigParser
from pyrogram import Client, filters
import aiofiles
import asyncpg
import psycopg2

config = ConfigParser()
config.read('config.ini')

api_id = config.get('pyrogram', 'api_id')
api_hash = config.get('pyrogram', 'api_hash')
db_name = config.get('postgresql', 'dbname')
db_user = config.get('postgresql', 'user')
db_pass = config.get('postgresql', 'password')
db_host = config.get('postgresql', 'host')
app = Client(name='my_account', api_id=api_id, api_hash=api_hash)


# Проверка на наличие таблицы "users"
try:
    conn = psycopg2.connect(dbname=db_name,
                            user=db_user,
                            password=db_pass,
                            host=db_host)

    with conn.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users(
            id bigint PRIMARY KEY,
            created_at TIMESTAMP,
            status char(10),
            status_updated_at TIMESTAMP,
            count_message int)'''
        )
        conn.commit()
except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)
finally:
    if conn:
        conn.close()

metadata = MetaData()
engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}')
users_table = Table('users', metadata,
                    Column('id', BigInteger, primary_key=True),
                    Column('created_at', DateTime),
                    Column('status', String),
                    Column('status_updated_at', DateTime),
                    Column('count_message', Integer)
                    )


@app.on_message(filters=filters.private)
async def auto_answer(client, message):
    users = {}
    with engine.connect() as connect:
        select_query = users_table.select()
        results = connect.execute(select_query)
        for row in results:
            users[row[0]] = row[1:]

        # Если пользователя нет в БД
        if message.chat.id not in users:
            insert_query = users_table.insert().values(
                id=int(message.chat.id),
                created_at=datetime.now(),
                status='alive',
                status_updated_at=datetime.now(),
                count_message=1
            )
            connect.execute(insert_query)
            connect.commit()

            if message.from_user.id == (await app.get_me()).id:
                pass
            else:
                await sleep(360) # 6 минут
                await app.send_message(chat_id=message.chat.id, text='Текст1')
        
        # Если пользователь есть в БД
        else:
            text_low = message.text.lower()
            status = users[message.chat.id][1].strip()
            count_message = users[message.chat.id][3]
            if status == 'alive':
                if "прекрасно" in text_low or "ожидать" in text_low:
                    update_query = users_table.update().where(users_table.c.id == int(message.chat.id)).values(
                        status='finished',
                        status_updated_at=datetime.now())
                    connect.execute(update_query)
                    connect.commit()
                elif "триггер1" in text_low:
                    update_query = users_table.update().where(users_table.c.id == int(message.chat.id)).values(
                        count_message=3,
                        status='finished',
                        status_updated_at=datetime.now())
                    connect.execute(update_query)
                    connect.commit()
                    await sleep(86400) # 1 день 2 часа
                    await app.send_message(chat_id=message.chat.id, text='Текст3')
                else:
                    count_message += 1
                    if count_message == 2:
                        update_query = users_table.update().where(users_table.c.id == int(message.chat.id)).values(
                            count_message=count_message)
                        connect.execute(update_query)
                        connect.commit()
                        await sleep(2340) # 39 минут
                        await app.send_message(chat_id=message.chat.id, text='Текст2')
                    if count_message == 3:
                        update_query = users_table.update().where(users_table.c.id == int(message.chat.id)).values(
                            status='finished',
                            count_message=count_message)
                        connect.execute(update_query)
                        connect.commit()
                        await sleep(86400) # 1 день 2 часа
                        await app.send_message(chat_id=message.chat.id, text='Текст3')

app.run()
