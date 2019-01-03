import asynctest
import model
import orm

sql_config = dict(host='localhost',
                  port=3306,
                  user='root',
                  password='Root!!2018',
                  db='litemall',
                  charset='utf8',
                  autocommit=True,
                  maxsize=10,
                  minsize=1,
                  )


class TestLitemallGoodsProduct(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))
        

    async def test_create(self):
        e1 = model.LitemallGoodsProduct(
            goods_id = 1,
            spec_id = "tests",
            price = 1.1111,
            number = 1000,
            add_time = "2011-01-11",
            updated_at = "2015-11-11"
        )
        await e1.save()
        e2 = await model.LitemallGoodsProduct.find_by(id = e1.id)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = model.LitemallGoodsProduct(
            goods_id = 2,
            spec_id = "tests",
            price = 1.1111,
            number = 1000,
            add_time = "2011-01-11",
            updated_at = "2015-11-11"
        )
        await e1.save()
        self.assertEqual(e1.price, 1.1111)
        e1.price = 2.0
        await e1.save()
        e2 = await model.LitemallGoodsProduct.find_by(id = e1.id)
        self.assertEqual(e2.price, 2.0)
        await e2.delete()

    async def high_query(self):
        res = model.LitemallGoodsProduct.query().where(orm.AND_(model.LitemallGoodsProduct.goods_id == 1,
                                                                model.LitemallGoodsProduct.number == 1000)).order('id', True).limit(1)
        self.assertEqual(len(res), 1)

    async def test_delete(self):
        e1 = await model.LitemallGoodsProduct.find_by(goods_id = 1)
        tmp = e1.id
        await e1.delete()

        e2 = await model.LitemallGoodsProduct.find_by(id = tmp)
        self.assertIsNone(e2, None)

