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
        pass


class String(Field):

    def __init__(self, legth, primary_key=False, default=None):
        super().__init__(type="varchar({})".format(str(legth)), primary_key=primary_key, default=default)


class Integer(Field):

    def __init__(self, primary_key=False, default=None):
        super().__init__(type="int(11)", primary_key=primary_key, default=default)


class Text(Field):

    def __init__(self, primary_key=False, default=None):
        super().__init__(type="mediumtext", primary_key=primary_key, default=default)

