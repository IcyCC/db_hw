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


class TestLitemallFootprint(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))
        self.loop.run_until_complete(orm.conn.execute(None,
            "TRUNCATE TABLE litemall_footprint"
        ))

    async def test_create(self):
        for i in range(5):
            await model.LitemallFootprint(
                user_id = i,
                goods_id = 5 - i
            ).save()
        result = list()
        result = await model.LitemallFootprint.all()
        self.assertEqual(len(result),5)

    async def test_update(self):
        for i in range(5):
            await model.LitemallFootprint(
                user_id = i,
                goods_id = 5 - i
            ).save()
        e1 = await model.LitemallFootprint.find_by(id=4)
        e1.goods_id = 8
        await e1.save()
        e2 = await model.LitemallFootprint.find_by(id=4)
        self.assertEqual(e2.goods_id, 8)

    async def test_delete(self):
        for i in range(5):
            await model.LitemallFootprint(
                user_id = i,
                goods_id = 5 - i
            ).save()
        e1 = await model.LitemallFootprint.find_by(id=3)
        await e1.delete()
        e2 = await model.LitemallFootprint.find_by(id=3)
        self.assertIsNone(e2, None)

    async def test_high_query(self):
        for i in range(5):
            await model.LitemallFootprint(
                user_id = i,
                goods_id = 5 - i
            ).save()
        sql = model.LitemallFootprint.query().where(model.LitemallFootprint.user_id <= 3)
        res = await sql.fetch()
        self.assertEqual(len(res), 4)