import asyncio
from . import conn


class Transaction(object):
    """
    全局事务管理
    """

    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self

    async def __aexit__(self, exctype, exc, tb):
        if exc is None:
            print("commit")
            await self.commit()
        else:
            print("rollback")
            await self.roll_back()
        return True         #阻止继续抛出错误

    @classmethod
    async def begin(cls):
        con = await conn.get_conn()
        await con.begin()
        return Transaction(con)

    async def commit(self):
        await self.conn.commit()
        self.conn.close()

    async def roll_back(self):
        await self.conn.rollback()
        self.conn.close()
