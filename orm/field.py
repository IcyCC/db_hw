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


class MultiCond(Cond):
    def __init__(self, logic, *conds):
        self._sql = " ( " + conds[0].sql() + " "
        self._args = conds[0].args()
        for i in range(1, len(conds)):
            self._sql +=  " " + logic + " " + conds[i].sql() + " "
            self._args += conds[i].args()
        self._sql += " ) "

    def sql(self):
        return self._sql

    def args(self):
        return self._args


def AND_(*conds):
    return MultiCond("AND", *conds)

def OR_(*conds):
    return MultiCond("OR", *conds)

def XOR_(*conds):
    return MultiCond("XOR", *conds)


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

    def sql(self):
        return self.name

    def args(self):
        return []

    def __eq__(self, other) -> Cond:
        return Cond(self.name, "=", other)

    def __ne__(self, other) -> Cond:
        return Cond(self.name, "<>", other)

    def __lt__(self, other) -> Cond:
        return Cond(self.name, "<", other)

    def __le__(self, other) -> Cond:
        return Cond(self.name, "<=", other)

    def __gt__(self, other) -> Cond:
        return Cond(self.name, ">", other)

    def __ge__(self, other) -> Cond:
        return Cond(self.name, ">=", other)


class String(Field):

    def __init__(self, length, primary_key=False, default=None):
        super().__init__(type="varchar({})".format(str(length)), primary_key=primary_key, default=default)


class Integer(Field):

    def __init__(self, length=11, primary_key=False, default=None):
        super().__init__(type="int({})".format(str(length)), primary_key=primary_key, default=default)


class Text(Field):

    def __init__(self, primary_key=False, default=None):
        super().__init__(type="mediumtext", primary_key=primary_key, default=default)


class TinyInteger(Field):

    def __init__(self, length, primary_key=False, default=None):
        super().__init__(type="tinyint({})".format(str(length)), primary_key=primary_key, default=default)


class Datetime(Field):

    def __init__(self, primary_key=False, default=None):
        super().__init__(type="datetime", primary_key=primary_key, default=default)


class Float(Field):

    def __init__(self, length=11, dec=4, primary_key=False, default=None):
        super().__init__(type="float({},{})".format(str(length), str(dec)))
