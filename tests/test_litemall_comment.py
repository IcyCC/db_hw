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


class TestLitemallComment(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.loop.run_until_complete(orm.conn.connection(
            loop=self.loop,
            **sql_config
        ))

    async def test_create(self):
        e1 = model.LitemallComment(
            content = '海星',
            user_id = 1,
            has_picture = 1,
            pic_urls = 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3630146112,3761050262&fm=27&gp=0.jpg',
            star = 3
        )
        await  e1.save()
        e2 = await model.LitemallComment.find_by(id=e1.id)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = model.LitemallComment(
            content = '海星',
            user_id = 2,
            has_picture = 1,
            pic_urls = 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3630146112,3761050262&fm=27&gp=0.jpg',
            star = 3
        )
        await  e1.save()
        e1 = await  model.LitemallComment.find_by(user_id = 2)
        e1.content = 'tests'
        await e1.save()
        e2 = await model.LitemallComment.find_by(user_id = 2)
        self.assertEqual(e2.content, 'tests')

    async def high_query(self):
        res = model.LitemallComment.query().where(
            orm.AND_(
                model.LitemallComment.content.in_(['海星', 'owrow']),
                model.LitemallComment.star.in_([1,2,3,4])
            )
        ).order('id', True).limit(1)
        self.assertEqual(len(res), 1)

    async def test_delete(self):
        e1 = await model.LitemallComment.find_by(user_id = 1)
        await e1.delete()
        e2 = await model.LitemallComment.find_by(id=e1.id)
        self.assertIsNone(e2, None)

