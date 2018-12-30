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
    sql = User.query().where(User.id > 1).order(User.id, True).limit(10)
    return await sql.fetch()

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
async await Transaction.begin() as tx:
    await u1.save(tx)
    await u2.save(tx)
```


### 索引支持

```python
name = orm.String(length=32, index='idx_users_name(32)')

```
