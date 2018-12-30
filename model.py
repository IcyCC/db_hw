from orm import orm
<<<<<<< HEAD
import asyncio

class Templ(orm.Model):
    __tablename__ = 'emacs'
    id = orm.Integer(length=11)
    name = orm.String(length=32)
=======



class Templ(orm.Model):
    __tablename__ = 'emacs'
    id = orm.Integer()
    name = orm.String(legth=32)

>>>>>>> 增加表
