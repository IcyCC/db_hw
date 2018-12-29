
class Transaction(object):
    """
    全局事务管理
    """
    @classmethod
    async def begin(cls):
        pass

    async def commit(self):
        pass

    async def roll_back(self):
        pass
