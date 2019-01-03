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


class TestLitemallCart(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))

    async def test_create(self):
        e1 = model.LitemallCart(
            user_id = 1,
            goods_id = 1,
            goods_sn = "test",
            goods_name = "test goods_name",
            product_id = 1,
            price = 100,
            number = 100
        )
        await e1.save()
        e2 = await model.LitemallCart.find_by(id = e1.id)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = model.LitemallCart(
            user_id = 1,
            goods_id = 1,
            goods_sn = "test",
            goods_name = "test goods_name",
            product_id = 1,
            price = 100,
            number = 100
        )
        await e1.save()
        self.assertEqual(e1.price, 100)
        e1.price = 200
        await e1.save()
        e2 = await model.LitemallCart.find_by(id = e1.id)
        self.assertEqual(e2.price, 200)
        await e2.delete()

    async def high_query(self):
        res = model.LitemallCart.query().where(orm.AND_(model.LitemallCart.user_id == 1,
                                                        orm.NOT_(model.LitemallCart.goods_price == 5500))).order('id', True).limit(1)
        self.assertEqual(len(res), 0)

    async def test_delete(self):
        e1 = await model.LitemallCart.find_by(user_id = 1)
        await e1.delete()

        e2 = await model.LitemallCart.find_by(id = e1.id)
        self.assertIsNone(e2, None)

