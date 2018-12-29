from orm import orm


class Shop(orm.Model):
    ___tablename__= 'shops'
    id = orm.Integer()

