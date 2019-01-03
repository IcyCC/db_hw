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


class TestLitemallGoods(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))

    async def test_create(self):
        e1 = model.LitemallGoods(
            goods_sn = '0000001',
            name = '球鞋',
            category_id = 1,
            brand_id = 1,
            brief = 'tests for brief',
            is_on_sale = 1
        )
        await e1.save()
        e2 = await model.LitemallGoods.find_by(id = e1.id)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = model.LitemallGoods(
            goods_sn = '0000001',
            name = '球鞋',
            category_id = 1,
            brand_id = 1,
            brief = 'tests for brief',
            is_on_sale = 1
        )
        await e1.save()
        self.assertEqual(e1.category_id, 1)
        e1.category_id = 200
        await e1.save()
        e2 = await model.LitemallGoods.find_by(id = e1.id)
        self.assertEqual(e2.category_id, 200)
        await e2.delete()

    async def high_query(self):
        res = model.LitemallGoods.query().where(orm.OR_(model.LitemallGoods.category_id == 1,
                                                         model.LitemallGoods.brand_id == 0)).order('id', True).limit(1)
        self.assertEqual(len(res), 1)

    async def test_delete(self):
        e1 = await model.LitemallGoods.find_by(category_id = 1)
        await e1.delete()

        e2 = await model.LitemallGoods.find_by(id = e1.id)
        self.assertIsNone(e2, None)

