import asyncpg
from typing import Optional
from dotenv import load_dotenv
import os

from datetime import datetime, timezone
from models.message import Message
from models.group import Group
from models.user import User
from models.messageBoard import MessageBoard

load_dotenv()
uri = os.getenv("POSTGRES_URL")

async def getTime():
    dt = datetime.now(timezone.utc)
    res = dt.replace(tzinfo=None)
    return res

class Database:
    # Basic
    def __init__(self):
        self.dsn = uri
        self.pool: Optional[asyncpg.Pool] = None
    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=1, max_size=10)
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
    async def get_server_version(self):
        async with self.pool.acquire() as conn:
            return await conn.get_server_version()

    # mboard
    async def return_messageBoards(self):
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT * FROM board")
    async def return_messageBoard(self, mboard_id):
        async with self.pool.acquire() as conn:
            return await conn.fetch(f"""SELECT * FROM board WHERE id={mboard_id}""")
    async def return_userJoinedMessageBoards(self, user_id):
        async with self.pool.acquire() as conn:
            groups = await conn.fetch(f"""SELECT id FROM group WHERE members LIKE '{user_id}'""")
            return await conn.fetch(f"""SELECT * FROM board WHERE members IN ({groups})""")
    async def create_messageBoard(self, mboard: MessageBoard):
        async with self.pool.acquire() as conn:
            sql_mboard = await mboard.toSql()
            return await conn.fetch(f"""INSERT INTO message VALUES ({sql_mboard})""")


    # message
    async def return_messageBoardMessages(self, mboard_id):
        async with self.pool.acquire() as conn:
            return await conn.fetch(f"""SELECT * FROM message WHERE messageBoard='{mboard_id}'""")
    async def return_userMessages(self, user_id):
        async with self.pool.acquire() as conn:
            return await conn.fetch(f"""SELECT * FROM message WHERE sender='{user_id}'""")
    async def create_message(self, message: Message):
        async with self.pool.acquire() as conn:
            sql_message = await message.toSql()
            return await conn.fetch(f"""INSERT INTO message (text, sender, timestamp, messageBoard) VALUES ({sql_message})""")

    # user
    async def return_users(self):
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT * FROM user")
    async def return_userById(self, user_id):
        async with self.pool.acquire() as conn:
            return await conn.fetch(f"""SELECT * FROM user WHERE id='{user_id}'""")
    async def return_userByName(self, user_name):
        async with self.pool.acquire() as conn:
            return await conn.fetch(f"""SELECT * FROM user WHERE id ='{user_name}'""")

    # group
    async def return_groups(self):
        async with self.pool.acquire() as conn:
            #return await conn.fetch("SELECT * FROM board WHERE members in ({groups})")
            return "1111"
    async def return_group(self, group_id):
        async with self.pool.acquire() as conn:
            #return await conn.fetch("SELECT * FROM board WHERE members in ({groups})")
            return "2222"
    async def return_groupsUser(self, user_id):
        async with self.pool.acquire() as conn:
            return await conn.fetch(f"""SELECT id FROM group WHERE members LIKE '{user_id}'""")
    async def create_group(self, group: Group):
        async with self.pool.acquire() as conn:
            sql_group = await group.toSql()
            return await conn.fetch(f"""INSERT INTO group (name, members) VALUES ({sql_group})""")

db = Database()
