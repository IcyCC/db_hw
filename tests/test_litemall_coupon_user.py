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


class TestLitemallCouponUser(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))
        

    async def test_create(self):
        e1 = model.LitemallCouponUser(
                user_id = 1,
                coupon_id = 1,
                status = 0,
        )
        await  e1.save()
        e2 = await model.LitemallCouponUser.find_by(id = e1.id)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = model.LitemallCouponUser(
            user_id = 2,
            coupon_id = 1,
            status = 0,
        )
        await  e1.save()
        e1 = await  model.LitemallCouponUser.find_by(user_id = 2)
        e1.status = 1
        await e1.save()
        e2 = await model.LitemallCouponUser.find_by(id = e1.id)
        self.assertEqual(e2.status, 1)

    async def high_query(self):
        res = model.LitemallCouponUser.query().where(orm.NOT_(model.LitemallCouponUser.user_id.between(0, 100))).order('id', True).limit(1)
        self.assertEqual(len(res), 0)

    async def test_delete(self):
        e1 = await model.LitemallCouponUser.find_by(user_id = 1)
        tmp = e1.id;
        await e1.delete()

        e2 = await model.LitemallCouponUser.find_by(id = tmp)
        self.assertIsNone(e2, None)

