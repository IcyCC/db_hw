from orm import orm


class Templ(orm.Model):
    __tablename__ = 'templs'
    id = orm.Integer(primary_key=True)
    name = orm.String(length=32)


class LitemallFootPrints(orm.Model):
    __tablename__ = 'litemall_foot_prints'
    id = orm.Integer(primary_key=True)
    user_id = orm.Integer()
    goods_id = orm.Integer()
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallAdmin(orm.Model):
    __tablename__ = 'litemall_admin'
    id = orm.Integer(primary_key=True)
    username = orm.String(length=63)
    password = orm.String(length=63)
    last_login_ip = orm.String(length=63)
    last_login_time = orm.Datetime()
    avatar = orm.String(length=255)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallAddress(orm.Model):
    __tablename__ = 'litemall_address'
    id = orm.Integer(primary_key=True)
    name = orm.String(length=63)
    user_id = orm.Integer()
    address = orm.String(length=127)
    mobile = orm.String(length=20)
    is_default = orm.TinyInteger(length=1)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallGoodsSpecification(orm.Model):
    __tablename__ = 'litemall_goods_specification'
    id = orm.Integer(primary_key=True)
    goods_id = orm.Integer()
    specification = orm.String(length=255)
    value = orm.String(length=255)
    pic_url = orm.String(length=255)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallBrand(orm.Model):
    __tablename__ = 'litemall_brand'
    id = orm.Integer(primary_key=True)
    name = orm.String(length=255)
    desc = orm.String(length=255)
    pic_url = orm.String(length=255)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallCollect(orm.Model):
    __tablename__ = 'litemall_collect'
    id = orm.Integer(primary_key=True)
    user_id = orm.Integer()
    value_id = orm.Integer()
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallOrderGoods(orm.Model):
    __tablename__ = 'litemall_order_goods'
    id = orm.Integer(primary_key=True)
    order_id = orm.Integer()
    goods_id = orm.Integer()
    goods_name = orm.String(length=127)
    goods_sn = orm.String(length=63)
    product_id = orm.Integer()
    number = orm.Integer()
    price = orm.Float()
    pic_url = orm.String(length=255)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallCategory(orm.Model):
    __tablename__ = 'litemall_category'
    id = orm.Integer(primary_key=True)
    name = orm.String(length=63)
    keywords = orm.String(length=1023)
    desc = orm.String(length=255)
    pid = orm.Integer()
    icon_url = orm.String(length=255)
    pic_url = orm.String(length=255)
    level = orm.String(length=255)
    sort_order = orm.TinyInteger(length=3)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallComment(orm.Model):
    __tablename__ = 'litemall_comment'
    id = orm.Integer(primary_key=True)
    content = orm.String(length=1023)
    user_id = orm.Integer()
    has_picture = orm.TinyInteger(length=1)
    pic_urls = orm.String(length=1023)
    star = orm.Integer()
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallCouponUser(orm.Model):
    __tablename__ = 'litemall_coupon_user'
    id = orm.Integer(primary_key=True)
    user_id = orm.Integer()
    coupon_id = orm.Integer()
    status = orm.Integer()
    used_time = orm.Datetime()
    start_time = orm.Datetime()
    end_time = orm.Datetime()
    order_id = orm.Integer()
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallGoodsProduct(orm.Model):
    __tablename__ = 'litemall_goods_product'
    id = orm.Integer(primary_key=True)
    goods_id = orm.Integer()
    specification = orm.String(length=255)
    price = orm.Float()
    number = orm.Integer()
    url = orm.String(length=125)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallOrder(orm.Model):
    __tablename__ = 'litemall_order'
    id = orm.Integer(primary_key=True)
    user_id = orm.Integer()
    order_sn = orm.String(length=63)
    order_status = orm.Integer()
    consignee = orm.String(length=63)
    mobile = orm.String(length=63)
    address = orm.String(length=127)
    message = orm.String(length=512)
    goods_price = orm.Float()
    freight_price = orm.Float()
    coupon_price = orm.Float()
    order_price = orm.Float()
    ship_sn = orm.String(length=63)
    ship_channel = orm.String(length=63)
    ship_time = orm.Datetime()
    confirm_time = orm.Datetime()
    end_time = orm.Datetime()
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallCoupon(orm.Model):
    __tablename__ = 'litemall_coupon'
    id = orm.Integer(primary_key=True)
    name = orm.String(length=63)
    desc = orm.String(length=127)
    tag = orm.String(length=63)
    total = orm.Integer()
    discount = orm.Float()
    min = orm.Float()
    limit = orm.Integer()
    type = orm.Integer()
    status = orm.Integer()
    goods_type = orm.Integer()
    goods_valus = orm.String(length=1023)
    code = orm.String(length=63)
    time_type = orm.Integer()
    days = orm.Integer()
    start_time = orm.Datetime()
    end_time = orm.Datetime()
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallGoods(orm.Model):
    __tablename__ = 'litemall_goods'
    id = orm.Integer(primary_key=True)
    goods_sn = orm.String(length=63)
    name = orm.String(length=127)
    category_id = orm.Integer()
    brand_id = orm.Integer()
    gallery = orm.String(length=1023)
    keywords = orm.String(length=255)
    brief = orm.String(length=255)
    is_on_sale = orm.TinyInteger(length=1)
    sort_order = orm.Integer()
    pic_url = orm.String(length=255)
    unit = orm.String(length=31)
    counter_price = orm.Float()
    retail_price = orm.Float()
    detail = orm.Text()
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallCart(orm.Model):
    __tablename__ = 'litemall_cart'
    id = orm.Integer(primary_key=True)
    user_id = orm.Integer()
    goods_id = orm.Integer()
    goods_sn = orm.String(length=63)
    goods_name = orm.String(length=127)
    product_id = orm.Integer()
    price = orm.Float()
    number = orm.Integer()
    checked = orm.TinyInteger(length=1)
    pic_url = orm.String(length=255)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)


class LitemallUser(orm.Model):
    __tablename__ = 'litemall_user'
    id = orm.Integer(primary_key=True)
    username = orm.String(length=63)
    password = orm.String(length=63)
    gender = orm.TinyInteger(length=3)
    birthday = orm.Datetime()
    last_login_time = orm.Datetime()
    last_login_ip = orm.String(length=63)
    nickname = orm.String(length=63)
    mobile = orm.String(length=20)
    avatar = orm.String(length=255)
    status = orm.TinyInteger(length=3)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.TinyInteger(length=1)
