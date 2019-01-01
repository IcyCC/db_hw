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
	deleted_at = orm.TinyInteger()

class LiteMailAdmin(orm.Model)
	__tablename__ = 'litem_foot_prints'
	id = orm.Integer(primay_key=True)
	username = orm.String(length = 63)
	password = orm.String(length = 63)
	last_login_ip = orm.String(length = 63)
	last_login_time = orm.Datetime()
	avatar = orm.String(length = 255)
	add_time = orm.Datetime()
	update_at = orm.Datetime()
	deleted_at = orm.TinyInteger()

class LiteMailAddress(orm.Model)
	__tablename__ = 'litem_foot_prints'
	id = orm.Integer(primay_key=True)
	name = orm.String(length = 63)
	user_id = orm.Integer()
	address = orm.String(length = 127)
	mobile = orm.String(length = 20)
	is_default = orm.TinyInteger()
	add_time = orm.Datetime()
	update_at = orm.Datetime()
	deleted_at = TinyInteger()

class LiteMailGoodsSpecification(orm.Model)
	__tablename__ = 'litem_foot_prints'
	id = 

