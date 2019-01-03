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


class TestLitemallGoodsSpecification(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))
        self.loop.run_until_complete(orm.conn.execute(None,
                                                      "TRUNCATE TABLE litemall_goods_specification"
                                                      ))

    async def test_create(self):
        for i in range(5):
            await model.LitemallGoodsSpecification(
                goods_id=i,
                specification='test' + str(i),
                value='test',
                pic_url='test'
            ).save()
        result = list()
        result = await model.LitemallGoodsSpecification.all()
        self.assertEqual(len(result), 5)

    async def test_update(self):
        for i in range(5):
            await model.LitemallGoodsSpecification(
                goods_id=i,
                specification='test' + str(i),
                value='test',
                pic_url='test'
            ).save()
        e1 = await model.LitemallGoodsSpecification.find_by(id=4)
        e1.value = 'updated_value'
        await e1.save()
        e2 = await model.LitemallGoodsSpecification.find_by(id=4)
        self.assertEqual(e2.value, 'updated_value')

    async def test_delete(self):
        for i in range(5):
            await model.LitemallGoodsSpecification(
                goods_id=i,
                specification='test' + str(i),
                value='test',
                pic_url='test'
            ).save()
        e1 = await model.LitemallGoodsSpecification.find_by(id=3)
        await e1.delete()
        e2 = await model.LitemallGoodsSpecification.find_by(id=3)
        self.assertIsNone(e2, None)

    async def test_high_query(self):
        for i in range(5):
            await model.LitemallGoodsSpecification(
                goods_id=i,
                specification='test' + str(i),
                value='test',
                pic_url='test'
            ).save()
        sql = model.LitemallGoodsSpecification.query().where(orm.AND_(model.LitemallGoodsSpecification.value == 'test',
                                                                      model.LitemallGoodsSpecification.goods_id == 1))
        res = await sql.fetch()
        self.assertEqual(len(res), 1)
