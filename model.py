from orm import orm


class Templ(orm.Model):
    __tablename__ = 'emacs'
    id = orm.Integer()
    name = orm.String(legth=32)
