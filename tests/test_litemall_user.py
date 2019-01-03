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


class TestLitemallUser(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))

    async def test_create(self):
        e1 = model.LitemallUser(
            username = 'cyyzero',
            password = '1122432423',
            gender = 1,
            birthday = '1997-12-24',
            last_login_ip = '202.204.121.23',
            nickname = 'pluto',
            mobile = '154045866',
            avatar = 'https://asdf.sf',
            status = 0
        )
        await e1.save()
        e2 = await model.LitemallUser.find_by(id = e1.id)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = model.LitemallUser(
            username = 'cyyzero',
            password = '1122432423',
            gender = 1,
            birthday = '1997-12-24',
            last_login_ip = '202.204.121.23',
            nickname = 'pluto',
            mobile = '154045866',
            avatar = 'https://asdf.sf',
            status = 0
        )
        await e1.save()
        self.assertEqual(e1.status, 0)
        e1.status = 1
        await e1.save()
        e2 = await model.LitemallUser.find_by(id = e1.id)
        self.assertEqual(e2.status, 1)
        await e2.delete()

    async def high_query(self):
        res = model.LitemallUser.query().where(model.LitemallUser.username.in_(['cyyzero', 'xxxxx']))
        self.assertEqual(len(res), 1)

    async def test_delete(self):
        e1 = await model.LitemallUser.find_by(username = 'cyyzero')
        await e1.delete()

        e2 = await model.LitemallUser.find_by(id = e1.id)
        self.assertIsNone(e2, None)

