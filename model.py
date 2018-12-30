from orm import orm

import asyncio

l = asyncio.get_event_loop()
l.run_until_complete()

class Templ(orm.Model):
    __tablename__ = 'emacs'
    id = orm.Integer()
    name = orm.String(legth=32)

u = Templ(id=1)
u