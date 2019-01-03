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

