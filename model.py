import datetime
import orm
import asyncio


class Templ(orm.Model):
    __tablename__ = 'templs'
    id = orm.Integer(primary_key=True)
    name = orm.String(length=32)


class BaseModel(orm.Model):

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
        orm.event_bus.add_table_event(self,
                                      'CREATED', self.on_base_model_created)
        orm.event_bus.add_table_event(self,
                                      'UPDATED', self.on_base_model_update)

    id = orm.Integer(primary_key=True)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.Datetime()

    def on_base_model_created(self, event, *args, **kwargs):
        args[0].add_time = datetime.datetime.now()

    def on_base_model_update(self, event, *args, **kwargs):
        args[0].updated_at = datetime.datetime.now()


class LitemallFootprint(BaseModel):
    __tablename__ = 'litemall_footprint'
    user_id = orm.Integer()
    goods_id = orm.Integer()


class LitemallAdmin(BaseModel):
    __tablename__ = 'litemall_admin'
    username = orm.String(length=63)
    password = orm.String(length=63)
    last_login_ip = orm.String(length=63)
    last_login_time = orm.Datetime()
    avatar = orm.String(length=255)


class LitemallAddress(BaseModel):
    __tablename__ = 'litemall_address'
    name = orm.String(length=63)
    user_id = orm.Integer()
    address = orm.String(length=127)
    mobile = orm.String(length=20)
    is_default = orm.TinyInteger(length=1)


class LitemallGoodsSpecification(BaseModel):
    __tablename__ = 'litemall_goods_specification'
    goods_id = orm.Integer()
    specification = orm.String(length=255)
    value = orm.String(length=255)
    pic_url = orm.String(length=255)


class LitemallBrand(BaseModel):
    __tablename__ = 'litemall_brand'
    name = orm.String(length=255)
    description = orm.String(length=255)
    pic_url = orm.String(length=255)


class LitemallCollect(BaseModel):
    __tablename__ = 'litemall_collect'
    user_id = orm.Integer()
    value_id = orm.Integer()


class LitemallOrderGoods(BaseModel):
    __tablename__ = 'litemall_order_goods'
    order_id = orm.Integer()
    goods_id = orm.Integer()
    goods_name = orm.String(length=127)
    goods_sn = orm.String(length=63)
    product_id = orm.Integer()
    number = orm.Integer()
    price = orm.Float()
    pic_url = orm.String(length=255)


class LitemallCategory(BaseModel):
    __tablename__ = 'litemall_category'
    name = orm.String(length=63)
    keywords = orm.String(length=1023)
    description = orm.String(length=255)
    pid = orm.Integer()
    icon_url = orm.String(length=255)
    pic_url = orm.String(length=255)
    level = orm.String(length=255)
    sort_order = orm.TinyInteger(length=3)


class LitemallComment(BaseModel):
    __tablename__ = 'litemall_comment'
    content = orm.String(length=1023)
    user_id = orm.Integer()
    good_id = orm.Integer()
    has_picture = orm.TinyInteger(length=1)
    pic_urls = orm.String(length=1023)
    star = orm.Integer()


class LitemallCouponUser(BaseModel):
    __tablename__ = 'litemall_coupon_user'
    id = orm.Integer(primary_key=True)
    user_id = orm.Integer()
    coupon_id = orm.Integer()
    status = orm.Integer()
    used_time = orm.Datetime()
    start_time = orm.Datetime()
    end_time = orm.Datetime()
    order_id = orm.Integer()


class LitemallGoodsProduct(BaseModel):
    __tablename__ = 'litemall_goods_product'
    goods_id = orm.Integer()
    spec_id = orm.Integer()
    price = orm.Float()
    number = orm.Integer()
    url = orm.String(length=125)


class LitemallOrder(BaseModel):
    __tablename__ = 'litemall_order'
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


class LitemallCoupon(BaseModel):
    __tablename__ = 'litemall_coupon'
    name = orm.String(length=63)
    description = orm.String(length=127)
    tag = orm.String(length=63)
    total = orm.Integer()
    discount = orm.Float()
    min = orm.Float()
    limitation = orm.Integer()
    type = orm.Integer()
    status = orm.Integer()
    goods_type = orm.Integer()
    goods_value = orm.String(length=1023)
    code = orm.String(length=63)
    time_type = orm.Integer()
    days = orm.Integer()
    start_time = orm.Datetime()
    end_time = orm.Datetime()


class LitemallGoods(BaseModel):
    __tablename__ = 'litemall_goods'
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
    retail_price = orm.Float()
    detail = orm.Text()


class LitemallCart(BaseModel):
    __tablename__ = 'litemall_cart'
    user_id = orm.Integer()
    goods_id = orm.Integer()
    goods_sn = orm.String(length=63)
    goods_name = orm.String(length=127)
    product_id = orm.Integer()
    price = orm.Float()
    number = orm.Integer()
    checked = orm.TinyInteger(length=1)
    pic_url = orm.String(length=255)


class LitemallUser(BaseModel):
    __tablename__ = 'litemall_user'
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
