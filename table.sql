create table if not exists litemall_admin
(
  id              int auto_increment
    primary key,
  username        varchar(63) default ''    not null
  comment '管理员名称',
  password        varchar(63) default ''    not null
  comment '管理员密码',
  last_login_ip   varchar(63) default ''    null
  comment '最近一次登录IP地址',
  last_login_time datetime                  null
  comment '最近一次登录时间',
  avatar          varchar(255) default '''' null
  comment '头像图片',
  add_time        datetime                  null
  comment '创建时间',
  updated_at      datetime                  null
  comment '更新时间',
  deleted_at      datetime                  null
  comment '逻辑删除'
)
  comment '管理员表'
  charset = utf8mb4;

create table if not exists litemall_brand
(
  id          int auto_increment
    primary key,
  name        varchar(255) default '' not null
  comment '品牌商名称',
  description varchar(255) default '' not null
  comment '品牌商简介',
  pic_url     varchar(255) default '' not null
  comment '品牌商页的品牌商图片',
  add_time    datetime                null
  comment '创建时间',
  updated_at  datetime                null
  comment '更新时间',
  deleted_at  datetime                null
  comment '逻辑删除'
)
  comment '品牌商表'
  charset = utf8mb4;

create table if not exists litemall_category
(
  id          int auto_increment
    primary key,
  name        varchar(63) default ''    not null
  comment '类目名称',
  keywords    varchar(1023) default ''  not null
  comment '类目关键字，以JSON数组格式',
  description varchar(255) default ''   null
  comment '类目广告语介绍',
  pid         int default '0'           not null
  comment '父类目ID',
  icon_url    varchar(255) default ''   null
  comment '类目图标',
  pic_url     varchar(255) default ''   null
  comment '类目图片',
  level       varchar(255) default 'L1' null,
  sort_order  tinyint(3) default '50'   null
  comment '排序',
  add_time    datetime                  null
  comment '创建时间',
  updated_at  datetime                  null
  comment '更新时间',
  deleted_at  datetime                  null
  comment '逻辑删除',
  constraint litemall_category_litemall_category_id_fk
  foreign key (pid) references litemall_category (id)
)
  comment '类目表'
  charset = utf8mb4;

create index parent_idx
  on litemall_category (pid);

create table if not exists litemall_coupon
(
  id          int auto_increment
    primary key,
  name        varchar(63)                   not null
  comment '优惠券名称',
  description varchar(127) default ''       null
  comment '优惠券介绍，通常是显示优惠券使用限制文字',
  tag         varchar(63) default ''        null
  comment '优惠券标签，例如新人专用',
  total       int default '0'               not null
  comment '优惠券数量，如果是0，则是无限量',
  discount    decimal(10, 2) default '0.00' null
  comment '优惠金额，',
  min         decimal(10, 2) default '0.00' null
  comment '最少消费金额才能使用优惠券。',
  limitation  smallint(6) default '1'       null
  comment '用户领券限制数量，如果是0，则是不限制；默认是1，限领一张.',
  type        smallint(6) default '0'       null
  comment '优惠券赠送类型，如果是0则通用券，用户领取；如果是1，则是注册赠券；如果是2，则是优惠券码兑换；',
  status      smallint(6) default '0'       null
  comment '优惠券状态，如果是0则是正常可用；如果是1则是过期; 如果是2则是下架。',
  goods_type  smallint(6) default '0'       null
  comment '商品限制类型，如果0则全商品，如果是1则是类目限制，如果是2则是商品限制。',
  goods_value varchar(1023) default '[]'    null
  comment '商品限制值，goods_type如果是0则空集合，如果是1则是类目集合，如果是2则是商品集合。',
  code        varchar(63)                   null
  comment '优惠券兑换码',
  time_type   smallint(6) default '0'       null
  comment '有效时间限制，如果是0，则基于领取时间的有效天数days；如果是1，则start_time和end_time是优惠券有效期；',
  days        smallint(6) default '0'       null
  comment '基于领取时间的有效天数days。',
  start_time  datetime                      null
  comment '使用券开始时间',
  end_time    datetime                      null
  comment '使用券截至时间',
  add_time    datetime                      null
  comment '创建时间',
  updated_at  datetime                      null
  comment '更新时间',
  deleted_at  datetime                      null
  comment '逻辑删除'
)
  comment '优惠券信息及规则表'
  charset = utf8;

create table if not exists litemall_goods
(
  id           int auto_increment
    primary key,
  goods_sn     varchar(63) default ''             not null
  comment '商品编号',
  name         varchar(127) default ''            not null
  comment '商品名称',
  category_id  int default '0'                    null
  comment '商品所属类目ID',
  brand_id     int default '0'                    null,
  gallery      varchar(1023)                      null
  comment '商品宣传图片列表，采用JSON数组格式',
  keywords     varchar(255) default ''            null
  comment '商品关键字，采用逗号间隔',
  brief        varchar(255) default ''            null
  comment '商品简介',
  is_on_sale   tinyint(1) default '1'             null
  comment '是否上架',
  sort_order   smallint(4) default '100'          null,
  pic_url      varchar(255)                       null
  comment '商品页面商品图片',
  unit         varchar(31) default '’件‘'          null
  comment '商品单位，例如件、盒',
  retail_price decimal(10, 2) default '100000.00' null
  comment '零售价格',
  detail       text                               null
  comment '商品详细介绍，是富文本格式',
  add_time     datetime                           null
  comment '创建时间',
  updated_at   datetime                           null
  comment '更新时间',
  deleted_at   datetime                           null
  comment '逻辑删除',
  constraint litemall_goods_litemall_brand_id_fk
  foreign key (brand_id) references litemall_brand (id),
  constraint litemall_goods_litemall_category_id_fk
  foreign key (category_id) references litemall_category (id)
)
  comment '商品基本信息表'
  charset = utf8mb4;

create index brand_id_idx
  on litemall_goods (brand_id);

create index cat_id_idx
  on litemall_goods (category_id);

create index goods_sn_idx
  on litemall_goods (goods_sn);

create index sort_order_idx
  on litemall_goods (sort_order);

create table if not exists litemall_goods_product
(
  id            int auto_increment
    primary key,
  goods_id      int default '0'               not null
  comment '商品表的商品ID',
  spec_id int default '0'               not null
  comment '商品规格id',
  price         decimal(10, 2) default '0.00' not null
  comment '商品货品价格',
  number        int default '0'               not null
  comment '商品货品数量',
  url           varchar(125)                  null
  comment '商品货品图片',
  add_time      datetime                      null
  comment '创建时间',
  updated_at    datetime                      null
  comment '更新时间',
  deleted_at    datetime                      null
  comment '逻辑删除',
  constraint litemall_goods_product_litemall_goods_id_fk
  foreign key (goods_id) references litemall_goods (id)
)
  comment '商品货品表'
  charset = utf8mb4;

create table if not exists litemall_goods_specification
(
  id            int auto_increment
    primary key,
  goods_id      int default '0'         not null
  comment '商品表的商品ID',
  specification varchar(255) default '' not null
  comment '商品规格名称',
  value         varchar(255) default '' not null
  comment '商品规格值',
  pic_url       varchar(255) default '' not null
  comment '商品规格图片',
  add_time      datetime                null
  comment '创建时间',
  updated_at    datetime                null
  comment '更新时间',
  deleted_at    datetime                null
  comment '逻辑删除',
  constraint litemall_goods_specification_litemall_goods_id_fk
  foreign key (goods_id) references litemall_goods (id)
)
  comment '商品规格表'
  charset = utf8mb4;

create index goods_idx
  on litemall_goods_specification (goods_id);

create table if not exists litemall_order_goods
(
  id         int auto_increment
    primary key,
  order_id   int default '0'               not null
  comment '订单表的订单ID',
  goods_id   int default '0'               not null
  comment '商品表的商品ID',
  goods_name varchar(127) default ''       not null
  comment '商品名称',
  goods_sn   varchar(63) default ''        not null
  comment '商品编号',
  product_id int default '0'               not null
  comment '商品货品表的货品ID',
  number     smallint default '0'          not null
  comment '商品货品的购买数量',
  price      decimal(10, 2) default '0.00' not null
  comment '商品货品的售价',
  pic_url    varchar(255) default ''       not null
  comment '商品货品图片或者商品图片',
  add_time   datetime                      null
  comment '创建时间',
  updated_at datetime                      null
  comment '更新时间',
  deleted_at datetime                      null
  comment '逻辑删除',
  constraint litemall_order_goods_litemall_goods_id_fk
  foreign key (goods_id) references litemall_goods (id),
  constraint litemall_order_goods_litemall_goods_product_id_fk
  foreign key (product_id) references litemall_goods_product (id)
)
  comment '订单商品表'
  charset = utf8mb4;

create index goods_idx
  on litemall_order_goods (goods_id);

create index order_idx
  on litemall_order_goods (order_id);

create table if not exists litemall_user
(
  id              int auto_increment
    primary key,
  username        varchar(63)             not null
  comment '用户名称',
  password        varchar(63) default ''  not null
  comment '用户密码',
  gender          tinyint(3) default '0'  not null
  comment '性别：0 未知， 1男， 1 女',
  birthday        datetime                null
  comment '生日',
  last_login_time datetime                null
  comment '最近一次登录时间',
  last_login_ip   varchar(63) default ''  not null
  comment '最近一次登录IP地址',
  nickname        varchar(63) default ''  not null
  comment '用户昵称或网络名称',
  mobile          varchar(20) default ''  not null
  comment '用户手机号码',
  avatar          varchar(255) default '' not null
  comment '用户头像图片',
  status          tinyint(3) default '0'  not null
  comment '0 可用, 1 禁用, 2 注销',
  add_time        datetime                null
  comment '创建时间',
  updated_at      datetime                null
  comment '更新时间',
  deleted_at      datetime                null
  comment '逻辑删除',
  constraint user_name
  unique (username)
)
  comment '用户表'
  charset = utf8mb4;

create table if not exists litemall_address
(
  id         int auto_increment
    primary key,
  name       varchar(63) default ''  not null
  comment '收货人名称',
  user_id    int default '0'         not null
  comment '用户表的用户ID',
  address    varchar(127) default '' not null
  comment '具体收货地址',
  mobile     varchar(20) default ''  not null
  comment '手机号码',
  is_default tinyint(1) default '0'  not null
  comment '是否默认地址',
  add_time   datetime                null
  comment '创建时间',
  updated_at datetime                null
  comment '更新时间',
  deleted_at datetime                null
  comment '逻辑删除',
  constraint litemall_address_litemall_user_id_fk
  foreign key (user_id) references litemall_user (id)
)
  comment '收货地址表'
  charset = utf8mb4;

create index user_id
  on litemall_address (user_id);

create table if not exists litemall_cart
(
  id         int auto_increment
    primary key,
  user_id    int                           null
  comment '用户表的用户ID',
  goods_id   int                           null
  comment '商品表的商品ID',
  goods_sn   varchar(63)                   null
  comment '商品编号',
  goods_name varchar(127)                  null
  comment '商品名称',
  product_id int                           null
  comment '商品货品表的货品ID',
  price      decimal(10, 2) default '0.00' null
  comment '商品货品的价格',
  number     smallint default '0'          null
  comment '商品货品的数量',
  checked    tinyint(1) default '1'        null
  comment '购物车中商品是否选择状态',
  pic_url    varchar(255)                  null
  comment '商品图片或者商品货品图片',
  add_time   datetime                      null
  comment '创建时间',
  updated_at datetime                      null
  comment '更新时间',
  deleted_at datetime                      null
  comment '逻辑删除',
  constraint litemall_cart_litemall_goods_id_fk
  foreign key (goods_id) references litemall_goods (id),
  constraint litemall_cart_litemall_goods_product_id_fk
  foreign key (product_id) references litemall_goods_product (id),
  constraint litemall_cart_litemall_user_id_fk
  foreign key (user_id) references litemall_user (id)
)
  comment '购物车商品表'
  charset = utf8mb4;

create table if not exists litemall_collect
(
  id         int auto_increment
    primary key,
  user_id    int default '0' not null
  comment '用户表的用户ID',
  value_id   int default '0' not null
  comment '商品ID',
  add_time   datetime        null
  comment '创建时间',
  updated_at datetime        null
  comment '更新时间',
  deleted_at datetime        null
  comment '逻辑删除',
  constraint litemall_collect_litemall_goods_id_fk
  foreign key (value_id) references litemall_goods (id),
  constraint litemall_collect_litemall_user_id_fk
  foreign key (user_id) references litemall_user (id)
)
  comment '收藏表'
  charset = utf8mb4;

create index user_idx
  on litemall_collect (user_id);

create index value_idx
  on litemall_collect (value_id);

create table if not exists litemall_comment
(
  id          int auto_increment
    primary key,
  content     varchar(1023) collate utf8mb4_unicode_ci not null
  comment '评论内容',
  user_id     int default '0'                          not null
  comment '用户表的用户ID',
  has_picture tinyint(1) default '0'                   null
  comment '是否含有图片',
  pic_urls    varchar(1023)                            null
  comment '图片地址列表，采用JSON数组格式',
  star        smallint(6) default '1'                  null
  comment '评分， 1-5',
  add_time    datetime                                 null
  comment '创建时间',
  updated_at  datetime                                 null
  comment '更新时间',
  deleted_at  datetime                                 null
  comment '逻辑删除',
  good_id     int                                      null,
  constraint litemall_comment_litemall_goods_id_fk
  foreign key (good_id) references litemall_goods (id),
  constraint litemall_comment_litemall_user_id_fk
  foreign key (user_id) references litemall_user (id)
)
  comment '评论表'
  charset = utf8;

create table if not exists litemall_coupon_user
(
  id         int auto_increment
    primary key,
  user_id    int                     not null
  comment '用户ID',
  coupon_id  int                     not null
  comment '优惠券ID',
  status     smallint(6) default '0' null
  comment '使用状态, 如果是0则未使用；如果是1则已使用；如果是2则已过期；如果是3则已经下架；',
  used_time  datetime                null
  comment '使用时间',
  start_time datetime                null
  comment '有效期开始时间',
  end_time   datetime                null
  comment '有效期截至时间',
  order_id   int                     null
  comment '订单ID',
  add_time   datetime                null
  comment '创建时间',
  updated_at datetime                null
  comment '更新时间',
  deleted_at datetime                null
  comment '逻辑删除',
  constraint litemall_coupon_user_litemall_coupon_id_fk
  foreign key (coupon_id) references litemall_coupon (id),
  constraint litemall_coupon_user_litemall_user_id_fk
  foreign key (user_id) references litemall_user (id)
)
  comment '优惠券用户使用表'
  charset = utf8;

create table if not exists litemall_footprint
(
  id         int auto_increment
    primary key,
  user_id    int default '0' not null
  comment '用户表的用户ID',
  goods_id   int default '0' not null
  comment '浏览商品ID',
  add_time   datetime        null
  comment '创建时间',
  updated_at datetime        null
  comment '更新时间',
  deleted_at datetime        null
  comment '逻辑删除',
  constraint litemall_footprint_litemall_goods_id_fk
  foreign key (goods_id) references litemall_goods (id),
  constraint litemall_footprint_litemall_user_id_fk
  foreign key (user_id) references litemall_user (id)
)
  comment '用户浏览足迹表'
  charset = utf8mb4;

create table if not exists litemall_order
(
  id            int auto_increment
    primary key,
  user_id       int                     not null
  comment '用户表的用户ID',
  order_sn      varchar(63)             not null
  comment '订单编号',
  order_status  smallint(6)             not null
  comment '订单状态',
  consignee     varchar(63)             not null
  comment '收货人名称',
  mobile        varchar(63)             not null
  comment '收货人手机号',
  address       varchar(127)            not null
  comment '收货具体地址',
  message       varchar(512) default '' not null
  comment '用户订单留言',
  goods_price   decimal(10, 2)          not null
  comment '商品总费用',
  freight_price decimal(10, 2)          not null
  comment '配送费用',
  coupon_price  decimal(10, 2)          not null
  comment '优惠券减免',
  order_price   decimal(10, 2)          not null
  comment '订单费用， = goods_price + freight_price - coupon_price',
  ship_sn       varchar(63)             null
  comment '发货编号',
  ship_channel  varchar(63)             null
  comment '发货快递公司',
  ship_time     datetime                null
  comment '发货开始时间',
  confirm_time  datetime                null
  comment '用户确认收货时间',
  end_time      datetime                null
  comment '订单关闭时间',
  add_time      datetime                null
  comment '创建时间',
  updated_at    datetime                null
  comment '更新时间',
  deleted_at    datetime                null
  comment '逻辑删除',
  constraint litemall_order_litemall_user_id_fk
  foreign key (user_id) references litemall_user (id)
)
  comment '订单表'
  charset = utf8;

