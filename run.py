import asyncio
import orm

loop = asyncio.get_event_loop()

sql_config = dict(host='localhost',
                  port=3306,
                  user='root',
                  password='Root!!2018',
                  db='itemmail',
                  charset='utf8',
                  autocommit=True,
                  maxsize=10,
                  minsize=1,
                  )

loop.run_until_complete(orm.conn.connection(
    loop=loop,
    **sql_config
))


class Templ(orm.Model):
    __tablename__ = 'templs'
    id = orm.Integer(length=11, primary_key=True)
    name = orm.String(length=32)

t1 = Templ(name='a')
type(t1.name)
loop.run_until_complete(t1.save())