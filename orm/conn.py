import aiomysql
import logging
import asyncio

_pool = None


async def connection(loop,**sql_config):

    print("Mysql start connection : {} ".format(str()))
    global _pool
    _pool = await aiomysql.create_pool(
        host=sql_config.get('host', 'localhost'),
        port=sql_config.get('port', 3306),
        user=sql_config['user'],
        password=sql_config['password'],
        db=sql_config['db'],
        charset=sql_config.get('charset', 'utf8'),
        autocommit=sql_config.get('autocommit', True),
        maxsize=sql_config.get('maxsize', 10),
        minsize=sql_config.get('minsize', 1),
        loop=loop)


async def select(sql, args, size=None):
    logging.info("select sql:{} arg{} ".format(str(sql), str(args)))
    global _pool
    async with _pool.get() as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info("select size {} ".format(str(len(rs))))
        return rs


async def execute(tx=None, sql=None, args=None, size=None):
    global _pool
    logging.info(sql, str(args))
    if tx is None:
        async with _pool.get() as con:
            cur = await con.cursor()
            await cur.execute(sql.replace('?', '%s'), args or ())
            rs = cur.rowcount
            await cur.close()
            print("select size {} ".format(str(rs)))
    else:
        cur = tx.conn.cursor()
        await cur.execute(sql.replace('?', '%s'), args or ())
        rs = cur.rowcount
        await cur.close()
        print("select size {} ".format(str(rs)))
    return rs

async def get_conn():
    global _pool
    return await _pool.get()