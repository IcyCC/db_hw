class Cond(object):
    
    def __init__(self, field, op, value):
        """
        比较的条件
        :param field:
        :param op:
        :param value:
        """
        if op == "BETWEEN":
            self._sql = " ".join([op, "? AND ? "])
            self._args = value
            self._field = field
        elif op == "LIKE":
            self._sql = " ".join([op, value])
            self._args = []
            self._field = field
        elif op == "IN":
            self._sql = " " + op
            self._sql += " ( ? "
            for v in value[1:]:
                self._sql += ", ? "
            self._sql += ")"
            self._args = value
            self._field = field
        else:
            self._sql = " ".join([field, op, "?"]);
            self._args = [value]
            self._field = ""

    def sql(self):
        return self._field + " " + self._sql

    def args(self):
        return self._args

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

def NOT_(cond):
    cond._sql = " NOT " + cond._sql
    return cond

class Field(object):
    """
    处理字段相关逻辑
    """

    def __init__(self, type, primary_key=False, default=None, not_null=False):
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

    def between(self, begin, end):
        return Cond(self.name, "BETWEEN", [begin, end])

    def like(self, expr):
        return Cond(self.name, "LIKE", expr)

    def in_(self, args):
        return Cond(self.name, "IN", args)

class String(Field):

    def __init__(self, length, primary_key=False, default=None, not_null=False):
        super().__init__(type="varchar({})".format(str(length)), primary_key=primary_key, default=default, not_null=not_null)


class Integer(Field):

    def __init__(self, length=11, primary_key=False, default=None, not_null=False):
        super().__init__(type="int({})".format(str(length)), primary_key=primary_key, default=default, not_null=not_null)


class Text(Field):

    def __init__(self, primary_key=False, default=None, not_null=False):
        super().__init__(type="mediumtext", primary_key=primary_key, default=default, not_null=not_null)


class TinyInteger(Field):

    def __init__(self, length, primary_key=False, default=None, not_null=False):
        super().__init__(type="tinyint({})".format(str(length)), primary_key=primary_key, default=default, not_null=not_null)


class Datetime(Field):

    def __init__(self, primary_key=False, default=None, not_null=False):
        super().__init__(type="datetime", primary_key=primary_key, default=default, not_null=not_null)


class Float(Field):

    def __init__(self, length=11, dec=4, primary_key=False, default=None, not_null=False):
        super().__init__(type="float({},{})".format(str(length), str(dec)), not_null=not_null)
