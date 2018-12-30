class Cond(object):

    def __init__(self, field, op, value):
        """
        比较的条件
        :param field:
        :param op:
        :param value:
        """
        self.field = field
        self.op = op
        self.value = value

    def sql(self):
        return " ".join([self.field, self.op, "?"])

    def args(self):
        return [self.value] 


class Field(object):
    """
    处理字段相关逻辑
    """

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

    def __eq__(self, other) -> Cond:
        return Cond(self.name, "=",  other)

    def __ne__(self, other) -> Cond:
        return Cond(self.name, "<>", other)

    def __lt__(self, other) -> Cond:
        return Cond(self.name, "<",  other)

    def __le__(self, other) -> Cond:
        return Cond(self.name, "<=", other)

    def __gt__(self, other) -> Cond:
        return Cond(self.name, ">",  other)

    def __ge__(self, other) -> Cond:
        return Cond(self.name, ">=", other)

class String(Field):

    def __init__(self, length, primary_key=False, default=None):
        super().__init__(type="varchar({})".format(str(length)), primary_key=primary_key, default=default)


class Integer(Field):

    def __init__(self, length, primary_key=False, default=None):
        super().__init__(type="int({})".format(str(length)), primary_key=primary_key, default=default)


class Text(Field):

    def __init__(self, primary_key=False, default=None):
        super().__init__(type="mediumtext", primary_key=primary_key, default=default)


class TinyInteger(Field):

    def __init__(self, length, primary_key=False, default=None):
        super().__init__(type="tinyint({})".format(str(length)), primary_key=primary_key, default=default)


class Datetime(Field):

    def __init__(self, length, primary_key=False, default=None):
        super().__init__(type="datetime", primary_key=primary_key, default=default)


class Float(Field):

    def __init__(self, length, dec, primary_key=False, default=None):
        super().__init__(type="float({},{})".format(str(length), str(dec)))