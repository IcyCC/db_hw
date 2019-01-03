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


class TestLitemallOrderGoods(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))
        self.loop.run_until_complete(orm.conn.execute(None,
            "TRUNCATE TABLE litemall_order_goods"
        ))

    async def test_create(self):
        for i in range(5):
            await model.LitemallOrderGoods(
                order_id = i,
                goods_id = i,
                goods_name = 'test' + str(i),
                goods_sn = '00000' + str(i),
                product_id = i,
                number = 1,
                price = 3.88,
                pic_url = 'test.png'
            ).save()
        result = list()
        
        result = await model.LitemallOrderGoods.all()
        self.assertEqual(len(result),5)

    async def test_update(self):
        for i in range(5):
            await model.LitemallOrderGoods(
                order_id = i,
                goods_id = i,
                goods_name = 'test' + str(i),
                goods_sn = '00000' + str(i),
                product_id = i,
                number = 1,
                price = 3.88,
                pic_url = 'test.png'
            ).save()
        e1 = await model.LitemallOrderGoods.find_by(id=4)
        e1.goods_name = 'test_update_order_goods'
        await e1.save()
        e2 = await model.LitemallOrderGoods.find_by(id=4)
        self.assertEqual(e2.goods_name, 'test_update_order_goods')

    async def test_delete(self):
        for i in range(5):
            await model.LitemallOrderGoods(
                order_id = i,
                goods_id = i,
                goods_name = 'test' + str(i),
                goods_sn = '00000' + str(i),
                product_id = i,
                number = 1,
                price = 3.88,
                pic_url = 'test.png'
            ).save()
        e1 = await model.LitemallOrderGoods.find_by(id=3)
        await e1.delete()
        e2 = await model.LitemallOrderGoods.find_by(id=3)
        self.assertIsNone(e2, None)

    async def test_high_query(self):
        for i in range(5):
            await model.LitemallOrderGoods(
                order_id = i,
                goods_id = i,
                goods_name = 'test' + str(i),
                goods_sn = '00000' + str(i),
                product_id = i,
                number = 1,
                price = 3.88,
                pic_url = 'test.png'
            ).save()
        sql = model.LitemallOrderGoods.query().where(model.LitemallOrderGoods.goods_name == 'test4')
        res = await sql.fetch()
        self.assertEqual(len(res), 1)