from orm import orm
import asyncio

class Templ(orm.Model):
    __tablename__ = 'emacs'
    id = orm.Integer(length=11)
    name = orm.String(length=32)
