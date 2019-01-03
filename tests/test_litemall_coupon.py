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


class TestLitemallCoupon(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))

    async def test_create(self):
        e1 = model.LitemallCoupon(
            name = 'name_test',
            description = '优惠券',
            tag = '新人专用',
            total = 100,
            discount = 100,
            min = 1000,
            limitation = 3,
            type = 0,
            status = 0,
            goods_type = 0
        )
        await e1.save()
        e2 = await model.LitemallCoupon.find_by(id = e1.id)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = model.LitemallCoupon(
            name = 'name_test',
            description = '优惠券',
            tag = '新人专用',
            total = 100,
            discount = 100,
            min = 1000,
            limitation = 3,
            type = 0,
            status = 0,
            goods_type = 0
        )
        await e1.save()
        self.assertEqual(e1.total, 100)
        e1.total = 200
        await e1.save()
        e2 = await model.LitemallCoupon.find_by(id = e1.id)
        self.assertEqual(e2.total, 200)
        await e2.delete()

    async def high_query(self):
        res = model.LitemallCoupon.query().where(orm.NOT_(model.LitemallCoupon.description.in_(['优惠券', 'xxx']))).order('id', True).limit(1)
        self.assertEqual(len(res), 0)

    async def test_delete(self):
        e1 = await model.LitemallCoupon.find_by(limitation = 3)
        await e1.delete()

        e2 = await model.LitemallCoupon.find_by(id = e1.id)
        self.assertIsNone(e2, None)

