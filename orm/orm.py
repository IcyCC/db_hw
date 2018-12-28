import logging
from . import conn


class Field(object):

    def __init__(self, type, primary_key=False, default=None):
        self.name = None
        self.type = type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return "< {} {} {} >".format(self.__class__.__name__, self.name, self.type)

    @property
    def sql_column(self):
        column = "{} {} ".format(self.name, self.type)
        if self.primary_key is True:
            column = column + "PRIMARY KEY AUTO_INCREMENT "
        if self.default is not None:
            column = column + "DEFAULT {}".format(str(self.default))
        return column


class String(Field):

    def __init__(self, legth, primary_key=False, default=None):
        super().__init__(type="varchar({})".format(str(legth)), primary_key=primary_key, default=default)


class Integer(Field):

    def __init__(self, primary_key=False, default=None):
        super().__init__(type="int(11)", primary_key=primary_key, default=default)


class Text(Field):

    def __init__(self, primary_key=False, default=None):
        super().__init__(type="mediumtext", primary_key=primary_key, default=default)


class ModelMetaClass(type):

    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)

        mappings = dict()
        fields = list()
        primary_key = None
        for k,v in attrs.items():
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

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

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
            keys.append(str(k)+" = ? ")
            values.append(v)
        rows = await conn.execute("{} {} WHERE {} = ?".format(self.__update__, ','.join(keys), self.__primary_key__),
                                  args=values + [getattr(self, self.__primary_key__, None)])
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % rows)

    @classmethod
    async def create_table(cls, coding="utf-8"):
        colums =[v.sql_column for v in cls.__mappings__.values()]
        await conn.execute('CREATE TABLE {} ({});'.format(cls.__tablename__ , ','.join(colums)), args=None)
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
