import asynctest
import model


class TestTempl(asynctest.TestCase):
    use_default_loop = True

    async def test_create(self):
        e1 = model.Templ(id=1)
        await  e1.save()
        e2 = await model.Templ.find_by(id=1)
        self.assertEqual(e1.id, e2.id)

    async def test_update(self):
        e1 = await  model.Templ.find_by(id=1)
        e1.name = 'b'
        await e1.save()
        e2 = await model.Templ.find_by(id=2)
        self.assertEqual(e2.name, 'b')

    async def test_delete(self):
        e1 = model.Templ(id=2, name='c')
        await e1.save()
        await e1.delete()
        e2 = model.Templ.find_by(id=2)
        self.assertIsNone(e2, None)

    async def high_query(self):
        res = model.Templ.query().where(model.Templ.name == 'a').order('id', True).limit(1)
        self.assertEqual(len(res), 1)
