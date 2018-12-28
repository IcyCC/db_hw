import logging
from . import conn
from .feild import *


class PreQuery:
    """
    预查询对象 通过fetch执行
    """

    def __init__(self, table_name, sql='', args=None):
        """

        :param table_name: 表名
        :param action: 操作类型 一般为
        :param sql: 执行的sql
        :param args: 参数
        """
        if args is None:
            args = list()
        self._sql = 'SELECT '
        self._args = args
        self._table_name = table_name

    @property
    def sql(self):
        return self._sql

    @property.setter
    def sql(self, value):
        self._sql = self.sql + value

    @property
    def args(self):
        return self._args

    @property.setter
    def args(self, value: list):
        self._args.extend(value)

    def where(self, conds):
        """
        条件限制
        :param conds:
        :return: PreQuery
        """
        pass

    def limit(self, num):
        """
        数量限制
        :param num:
        :return: PreQuery
        """
        pass

    def order(self, filed, desc):
        """
        数量限制
        :param num:
        :return: PreQuery
        """
        pass

    async def fetch(self):
        rows = await conn.select(sql=self.sql, args=self._args, size=None)
        return rows


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

        if attrs.get('__tablename__', None) is None:
            attrs['__tablename__'] = str(name).lower()
        attrs['__primary_key__'] = primary_key
        attrs['__mappings__'] = mappings
        attrs['__select__'] = "SELECT * FROM {}".format(attrs['__tablename__'])
        attrs['__insert__'] = "INSERT INTO {}".format(attrs['__tablename__'])
        attrs['__update__'] = "UPDATE {} SET ".format(attrs['__tablename__'])

        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaClass):
    """
    模型基类
    """

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def query(cls):
        """
        进行更复杂的查询
        :return: PreQuery 对象
        """
        return PreQuery(cls.__tablename__)

    @classmethod
    async def find_by(cls, **kwargs):
        items = tuple(kwargs.items())
        key, value = items[0]
        rs = await conn.select("{} WHERE {} = ?".format(cls.__select__, key), value)
        if not rs:
            return None
        result = list()
        for r in rs:
            result.append(cls(**r))

        return result

    @classmethod
    async def all(cls):
        rs = await conn.select("{}".format(cls.__select__), args=None)
        if not rs:
            return None
        result = list()
        for r in rs:
            result.append(cls(**r))

        return result

    async def save(self):
        keys = list()
        mappings = self.__mappings__
        for key, column in mappings.items():
            if column.primary_key is True:
                continue
            keys.append(key)
        values = self.get_args_by_fields(keys)
        rows = await conn.execute("{}({}) VALUES ({})".format(self.__insert__, ','.join(keys),
                                                              self.create_args(len(keys))),
                                  values)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % rows)

    async def update(self, **kwargs):
        keys = list()
        values = list()
        for k, v in kwargs.items():
            keys.append(str(k) + " = ? ")
            values.append(v)
        rows = await conn.execute("{} {} WHERE {} = ?".format(self.__update__, ','.join(keys), self.__primary_key__),
                                  args=values + [getattr(self, self.__primary_key__, None)])
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % rows)


    async def delete(self):
        pass

    @classmethod
    async def create_table(cls, coding="utf-8"):
        colums = [v.sql_column for v in cls.__mappings__.values()]
        await conn.execute('CREATE TABLE {} ({});'.format(cls.__tablename__, ','.join(colums)), args=None)
        await conn.execute('ALTER TABLE {} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;'
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
            if v is None:
                raise Exception("value is None")
            values.append(v)
        return values
