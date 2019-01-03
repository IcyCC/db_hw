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


class TestLitemallOrder(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))
        

    async def test_create(self):
        e1 = model.LitemallOrder(
            user_id = 1,
            order_sn = '000001',
            order_status = 0,
            consignee = 'cyy',
            mobile = '15521255895',
            address = '北京市海淀区',
            message = 'test',
            goods_price = 5500,
            freight_price = 10,
            coupon_price = 0,
            order_price = 5510
        )
        await e1.save()
        e2 = await model.LitemallOrder.find_by(id = e1.id)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = model.LitemallOrder(
            user_id = 1,
            order_sn = '000001',
            order_status = 0,
            consignee = 'cyy',
            mobile = '15521255895',
            address = '北京市海淀区',
            message = 'test',
            goods_price = 5500,
            freight_price = 10,
            coupon_price = 0,
            order_price = 5510
        )
        await e1.save()
        self.assertEqual(e1.order_status, 0)
        e1.order_status = 2
        await e1.save()
        e2 = await model.LitemallOrder.find_by(id = e1.id)
        self.assertEqual(e2.order_status, 2)
        await e2.delete()

    async def high_query(self):
        res = model.LitemallOrder.query().where(model.LitemallOrder.user_id.between(0, 100)).order('id', True).limit(1)
        self.assertEqual(len(res), 1)

    async def test_delete(self):
        e1 = await model.LitemallOrder.find_by(user_id = 1)
        await e1.delete()

        e2 = await model.LitemallOrder.find_by(id = e1.id)
        self.assertIsNone(e2, None)

