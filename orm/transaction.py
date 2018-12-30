import asyncio
from . import conn

class Transaction(object):
    """
    全局事务管理
    """
    def __init__(self, conn):
        self.conn = conn
        

    @classmethod
    async def begin(cls):
        con = await conn.get_conn()
        return Transaction(con)

    async def commit(self):
        await self.conn.commit()
        await self.conn.close()

    async def roll_back(self):
        await self.conn.roll_back()
        await self.conn.close()
