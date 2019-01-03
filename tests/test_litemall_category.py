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
                  


class TestLitemallCategory(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))
        self.loop.run_until_complete(orm.conn.execute(None,
            "TRUNCATE TABLE litemall_category"
        ))

    async def test_create(self):
        for i in range(5):
            await model.LitemallCategory(
                name = 'test_category' + str(i),
                keywords = '{"test"}',
                description = 'testad',
                level = 'L2',
                pid = 0,
                icon_url = 'test.ico',
                pic_url = 'test.png',
                sort_order = 50,
                add_time = '2019-01-03',
                updated_at = '2019-01-03',
                deleted_at = 0
            ).save()
        result = list()
        result = await model.LitemallCategory.all()
        self.assertEqual(len(result),5)

    async def test_update(self):
        for i in range(5):
            await model.LitemallCategory(
                name = 'test_category' + str(i),
                keywords = '{"test"}',
                description = 'testad',
                level = 'L2',
                pid = 0,
                icon_url = 'test.ico',
                pic_url = 'test.png',
                sort_order = 50,
                add_time = '2019-01-03',
                updated_at = '2019-01-03',
                deleted_at = 0
            ).save()
        e1 = await model.LitemallCategory.find_by(id=4)
        e1.name = 'test_update_category'
        await e1.save()
        e2 = await model.LitemallCategory.find_by(id=4)
        self.assertEqual(e2.name, 'test_update_category')

    async def test_delete(self):
        for i in range(5):
            await model.LitemallCategory(
                name = 'test_category' + str(i),
                keywords = '{"test"}',
                description = 'testad',
                level = 'L2',
                pid = 0,
                icon_url = 'test.ico',
                pic_url = 'test.png',
                sort_order = 50,
                add_time = '2019-01-03',
                updated_at = '2019-01-03',
                deleted_at = 0
            ).save()
        e1 = await model.LitemallCategory.find_by(id=3)
        await e1.delete()
        e2 = await model.LitemallCategory.find_by(id=3)
        self.assertIsNone(e2, None)

    async def test_high_query(self):
        for i in range(5):
            await model.LitemallCategory(
                name = 'test_category' + str(i),
                keywords = '{"test"}',
                description = 'testad',
                level = 'L2',
                pid = 0,
                icon_url = 'test.ico',
                pic_url = 'test.png',
                sort_order = 50,
                add_time = '2019-01-03',
                updated_at = '2019-01-03',
                deleted_at = 0
            ).save()
        sql = model.LitemallCategory.query().where(model.LitemallCategory.description == 'testad').limit(2)
        res = await sql.fetch()
        self.assertEqual(len(res), 2)
