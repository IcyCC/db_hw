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


class TestTempl(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))

    async def test_create(self):
        e1 = model.Templ(name='test')
        await  e1.save()
        e2 = await model.Templ.find_by(id=e1.id)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = await  model.Templ.find_by(id=4)
        e1.name = 'b'
        await e1.save()
        e2 = await model.Templ.find_by(id=4)
        self.assertEqual(e2.name, 'b')

    async def test_delete(self):
        e1 = model.Templ(name='c')
        await e1.save()
        await e1.delete()
        e2 = await model.Templ.find_by(id=e1.id)
        self.assertIsNone(e2, None)

    async def test_high_query(self):
        sql = model.Templ.query().where(model.Templ.name == 'a').order('id', True).limit(1)
        res = await sql.fetch()
        self.assertEqual(len(res), 1)
