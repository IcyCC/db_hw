from orm import orm

class Templ(orm.Model):
    __tablename__ = 'emacs'
    id = orm.Integer()
    name = orm.String(legth=32)


class LiteMailFootPrints(orm.Model):
	__tablename__ = 'litem_foot_prints'
	id = orm.Integer(primay_key=True)
	user_id = orm.Integer()
	goods_id = orm.Integer()
	add_time = orm.Datetime()
	update_at = orm.Datetime()
	deleted_at = TinyInteger()

class LiteMailAdmin(orm.Model)
	__tablename__ = 'litem_foot_prints'
	id = orm.Integer(primay_key=True)
	user_name = orm.String(length = 63)
