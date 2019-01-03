# orm

## GET START

### 定义模型：

```python

class User(orm.Model):
    id = orm.Integer(primary_key=True)
    name = orm.String(length=32)
    
```

### 基本操作


```python

async def create():
    u = User(name='b')
    return await u.save()


async def update():
    u.id = 1
    return await u.save()
    
async def select():
    return await User.all()
    
async def delete():
    return await u.delete()

```

### 高级查询

```python

async def high_select():
    sql = User.query().where(orm.OR_(orm.AND_(orm.NOT_(User.id > 10),
                                              User.id < 100),
                                    User.id==10,
                                    User.name == "cyy")).order(User.id).limit(5)
    await sql.fetch()
    # do other works

    sql = User.query().where(User.id.between(1, 100)).order(User.id).limit(10)
    await sql.fetch()
    # do other works

    sql = User.query().where(orm.NOT_(User.id.between(1, 100))).order(User.id).limit(10)
    await sql.fetch()
    # do other works

    sql = User.query().where(User.id.in_([1,2,3,4,100]))
    await sql.fetch()
    # do other works

    sql = User.query().where(orm.AND_(orm.NOT_(User.id.in_([1,2,3,4,100])), User.id.in_([11,222])))
    await sql.fetch()
    # do other works

    sql = User.query().where(User.name.like("B%"))
    await sql.fetch()
    # do other works

    sql = User.query().where(orm.NOT_(User.name.like("B%")))
    await sql.fetch()
    # do other works

```

### 事务

```python

async def trans():
    tx =  await Transaction.begin()
    u1 = User(name='a')
    u2 = User(name='b')
    try:
        await u1.save(tx)
        await u2.save(tx)
    except Exception:
        tx.roll_back()
    else:
        tx.commit()
```
2
```python
async with await Transaction.begin() as tx:
    await u1.save(tx)
    await u2.save(tx)
```


### 索引支持

```python
name = orm.String(length=32, index='idx_users_name(32)')

```

### 软触发器 + 业务基础类

```python

class BaseModel(orm.Model):

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
        orm.event_bus.add_table_event(self,
                                      'CREATED', self.on_base_model_created)
        orm.event_bus.add_table_event(self,
                                      'UPDATED', self.on_base_model_update)

    id = orm.Integer(primary_key=True)
    add_time = orm.Datetime()
    updated_at = orm.Datetime()
    deleted_at = orm.Datetime()

    def on_base_model_created(self, event, *args, **kwargs):
        args[0].add_time = datetime.datetime.now()

    def on_base_model_update(self, event, *args, **kwargs):
        args[0].updated_at = datetime.datetime.now()


```
