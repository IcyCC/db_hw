import asynctest
import model
import orm

sql_config = dict(host='localhost',
                  port=3306,
                  user='root',
                  password='Root!!2018',
                  db='itemmail',
                  charset='utf8',
                  autocommit=True,
                  maxsize=10,
                  minsize=1,
                  )

                  


class TestLitemallAddress(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))
        self.loop.run_until_complete(orm.conn.execute(None,
            "TRUNCATE TABLE litemall_address"
        ))

    async def test_create(self):
        for i in range(5):
            await model.LitemallAddress(
                name = 'test_address' + str(i),
                user_id = i,
                address = 'someplace',
                mobile = '13112345678',
                is_default = 1
            ).save()
        result = list()
        result = await model.LitemallAddress.all()
        self.assertEqual(len(result),5)

    async def test_update(self):
        for i in range(5):
            await model.LitemallAddress(
                name = 'test_address' + str(i),
                user_id = i,
                address = 'someplace',
                mobile = '13112345678',
                is_default = 1
            ).save()
        e1 = await model.LitemallAddress.find_by(id=4)
        e1.name = 'test_update_address'
        await e1.save()
        e2 = await model.LitemallAddress.find_by(id=4)
        self.assertEqual(e2.name, 'test_update_address')

    async def test_delete(self):
        for i in range(5):
            await model.LitemallAddress(
                name = 'test_address' + str(i),
                user_id = i,
                address = 'someplace',
                mobile = '13112345678',
                is_default = 1
            ).save()
        e1 = await model.LitemallAddress.find_by(id=3)
        await e1.delete()
        e2 = await model.LitemallAddress.find_by(id=3)
        self.assertIsNone(e2, None)

    async def test_high_query(self):
        for i in range(5):
            await model.LitemallAddress(
                name = 'test_address' + str(i),
                user_id = i,
                address = 'someplace',
                mobile = '13112345678',
                is_default = 1
            ).save()
        sql = model.LitemallAddress.query().where(model.LitemallAddress.address == 'someplace').limit(3)
        res = await sql.fetch()
        self.assertEqual(len(res), 3)