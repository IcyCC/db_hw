import asyncio
import logging
import copy
from . import conn
from .field import *
from .event import event_bus, TriggerEvent

loop = asyncio.get_event_loop()


class ModelMetaClass(type):

    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)

        mappings = dict()
        fields = list()
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                fields.append(k)
                v.name = str(k)
                mappings[k] = v
                if v.primary_key is True:
                    primary_key = k

        for k in mappings.keys():
            attrs.pop(k)

        for b in bases:
            if b.__name__ == 'Model':
                continue
            base_mapping = getattr(b, '__mappings__', {})
            mappings.update(base_mapping)
            if not primary_key:
                primary_key = b.__primary_key__

        if attrs.get('__tablename__', None) is None:
            attrs['__tablename__'] = str(name).lower()
        attrs['__primary_key__'] = primary_key
        attrs['__mappings__'] = mappings
        attrs['__select__'] = "SELECT * FROM {} ".format(attrs['__tablename__'])
        attrs['__insert__'] = "INSERT INTO {} ".format(attrs['__tablename__'])
        attrs['__update__'] = "UPDATE {} SET ".format(attrs['__tablename__'])
        attrs['__delete_s__'] = "DELETE FROM {} ".format(attrs['__tablename__'])
        attrs['__count__'] = "SELECT COUNT(*) FROM {}".format(attrs['__tablename__'])

        return type.__new__(cls, name, bases, attrs)

    def __getattr__(cls, item):
        """
        用于Model.Field 方式获取字段
        :param item:
        :return:
        """
        return cls.__mappings__[item]


class Model(dict, metaclass=ModelMetaClass):
    """
    模型基类
    """

    def __init__(self, **kwargs):

        for k, v in self.__mappings__.items():
            if k not in kwargs:
                kwargs[k] = v.default

        super(Model, self).__init__(**kwargs)

    def __getattr__(self, item):
        return self.get(item, None)

    def __setattr__(self, key, value):
        event_bus.publish(TriggerEvent(
            self.__tablename__,
            key,
            'SET'
        ))
        self[key] = value

    @classmethod
    def query(cls):
        """
        进行更复杂的查询
        :return: PreQuery 对象
        """
        return PreQuery(cls)

    @classmethod
    async def find_by(cls, **kwargs):
        items = tuple(kwargs.items())
        key, value = items[0]
        rs = await conn.select("{} WHERE {} = ?".format(cls.__select__, key), value, 1)
        if not rs:
            return None
        result = list()
        for r in rs:
            result.append(cls(**r))
        if result:
            return result[0]
        else:
            return None

    @classmethod
    async def all(cls):
        rs = await conn.select("{}".format(cls.__select__), args=None)
        if not rs:
            return None
        result = list()
        for r in rs:
            result.append(cls(**r))

        return result

    async def save(self, tx=None):
        keys = list()
        mappings = self.__mappings__
        # 主键没有值 新增
        for key, column in mappings.items():
            if column.primary_key is True:
                continue
            keys.append(key)
        if getattr(self, self.__primary_key__, None) is None:

            event_bus.publish(TriggerEvent(self.__tablename__, '*', 'CREATED'), self)
            values = self.get_args_by_fields(keys)

            rows, rowid = await conn.execute(tx, "{}({}) VALUES ({})".format(self.__insert__, ','.join(keys),
                                                                             self.create_args(len(keys))),
                                             values)
            if getattr(self, self.__primary_key__, None) != rowid:
                setattr(self, self.__primary_key__, rowid)
        else:
            # 主键有值 更新
            update_keys = list()
            for k in keys:
                update_keys.append(str(k) + " = ? ")

            event_bus.publish(TriggerEvent(self.__tablename__, '*', 'UPDATED'), self)
            values = self.get_args_by_fields(keys)
            rows, rowid = await conn.execute(tx, "{} {} WHERE {} = ?".format(self.__update__,
                                                                             ','.join(update_keys),
                                                                             self.__primary_key__,
                                                                             ),
                                             values + [getattr(self, self.__primary_key__, None)])
        if rows < 1:
            logging.warning('failed to insert record: affected rows: %s' % str(rows))

    async def update(self, tx=None, **kwargs):
        keys = list()
        values = list()
        for k, v in kwargs.items():
            keys.append(str(k) + " = ? ")
            values.append(v)
        event_bus.publish(TriggerEvent(self.__tablename__, '*', 'UPDATE'), self)
        rows, rowid = await conn.execute(tx,
                                         "{} {} WHERE {} = ?".format(self.__update__, ','.join(keys),
                                                                     self.__primary_key__),
                                         args=values + [getattr(self, self.__primary_key__, None)])
        if getattr(self, self.__primary_key__, None) != rowid:
            setattr(self, self.__primary_key__, rowid)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % str(rows))

    async def delete(self, tx=None):
        primary_key = getattr(self, self.__primary_key__, None)
        if primary_key is None:
            # 主键没有值 
            return False
        else:
            # 主键有值 删除
            event_bus.publish(TriggerEvent(self.__tablename__, '*', 'DELTED'), self)
            rows = await conn.execute(tx, "{} WHERE {} = ?".format(self.__delete_s__, self.__primary_key__),
                                      [primary_key])
        if rows != 1:
            logging.warning('failed to delete record: affected rows: %s' % str(rows))

    @classmethod
    async def create_table(cls, coding="utf-8"):
        colums = [v.sql_column for v in cls.__mappings__.values()]
        await conn.execute(None, 'CREATE TABLE {} ({});'.format(cls.__tablename__, ','.join(colums)), args=None)
        await conn.execute(None, 'ALTER TABLE {} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;'
                           .format(cls.__tablename__), args=None)

    @staticmethod
    def create_args(legth):
        a = list()
        for i in range(legth):
            a.append('?')
        return ','.join(a)

    def get_args_by_fields(self, keys):
        values = list()
        for key in keys:
            v = getattr(self, key, None)
            values.append(v)
        return values


class PreQuery:
    """
    预查询对象 通过fetch执行
    """

    def __init__(self, model: ModelMetaClass, sql='', args=None):
        """
        :param model: 表名
        :param action: 操作类型 一般为
        :param sql: 执行的sql
        :param args: 参数
        """
        self._model = model
        if args is None:
            args = list()
        self._sql = sql
        self._args = args

    def sql(self):
        return self._sql

    def append_sql(self, value: str):
        self._sql = self._sql + value

    def args(self):
        return self._args

    def append_args(self, value: list):
        self._args.extend(value)

    def __str__(self):
        return self._sql

    def where(self, cond):
        """
        条件限制
        :param cond:
        :return: PreQuery
        """
        query = copy.copy(self)
        query.append_sql(" WHERE " + cond.sql())
        query.append_args(cond.args())
        return query

    def limit(self, num):
        """
        数量限制
        :param num:
        :return: PreQuery
        """
        num = int(num)
        query = copy.copy(self)
        query.append_sql(" limit " + str(num))
        return query

    def order(self, field, desc=False):
        """
        数量限制
        :param num:
        :return: PreQuery
        """
        query = copy.copy(self)
        if desc:
            query.append_sql(" ".join([" ORDER BY", field.name, "DESC "]))
        else:
            query.append_sql(" ".join([" ORDER BY", field.name, "ASC "]))
        return query

    async def fetch(self):
        rows = await conn.select(sql=self._model.__select__ + self.sql(), args=self.args(), size=None)
        result = list()
        for r in rows:
            result.append(self._model(**r))
        return result

    async def count(self):
        rows = await conn.select(sql=self._model.__count__ + self.sql(), args=self.args(), size=None)
        return rows[0].get('COUNT(*)', 0)
