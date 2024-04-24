# Simple SELECT
- https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select

With some rows in the database, here’s the simplest form of emitting a SELECT statement to load some objects. To create SELECT statements, we use the select() function to create a new Select object, which we then invoke using a Session. The method that is often useful when querying for ORM objects is the Session.scalars() method, which will return a ScalarResult object that will iterate through the ORM objects we’ve selected:


```
from sqlalchemy import select

session = Session(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

for user in session.scalars(stmt):
    print(user)
```



# select vs query
- https://stackoverflow.com/a/72847337/2897115

The biggest difference is how the select statement is constructed. The new method creates a select object which is more dynamic since it can be constructed from other select statements, without explicit subquery definition:

```
# select from a subqeuery styled query
q = select(Users).filter_by(name='name', email='mail@example.com')
q = select(Users.name, Users.email).select_from(q)
```
The outcome is more "native sql" construction of querying, as per the latest selectable API. Queries can be defined and passed throughout statements in various functionalities such as where clauses, having, select_from, intersect, union, and so on.



# simple example
- https://nikhilakki.in/dancing-with-data-an-intro-to-sqlalchemy-20-orm

```
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    # More fields and relationships here...
```


Adding new friends (users):

```
spongebob = User(name="spongebob", fullname="Spongebob Squarepants")
session.add(spongebob)
session.commit()
```


# Typed model classes

Here's a SQLAlchemy 2.0 model with typed columns:

```
class BlogPost(Base):
    __tablename__ = "blog_post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    content: Mapped[str]
```

When you're using an IDE that understands type annotations (like VS Code with the Python extension), you can then get intellisense for those columns, like suggestions for functions that can be called on that data type.

Screenshot of intellisense suggestion for id column

You can also run a tool like mypy or pyright to find out if any of your code is using types incorrectly. For example, imagine I wrote a function to process the BlogPost model above:

```
def process_blog_posts(posts: list[BlogPost]):
    for post in posts:
        post.title = post.title.upper()
        post.id = post.id.upper()
```
Then running mypy would let me know if my code was using the typed columns incorrectly:
```
$ python3 -m mypy main_sqlalchemy.py 
main_sqlalchemy.py:30: error: "int" has no attribute "upper"  [attr-defined]
```


# Embracing Modern Python for Web Development

https://dev.to/matib/embracing-modern-python-for-web-development-3nk7



# CORE and ORM

- https://docs.sqlalchemy.org/en/20/tutorial/index.html

SQLAlchemy is presented as two distinct APIs, one building on top of the other. These APIs are known as Core and ORM.

# sqlalchemy namespace  vs sqlalchemy.orm namespace

Sections that are primarily Core-only will not refer to the ORM. SQLAlchemy constructs used in these sections will be imported from the sqlalchemy namespace. 

Sections that are primarily ORM-only should be titled to include the phrase “ORM”, so that it’s clear this is an ORM related topic. SQLAlchemy constructs used in these sections will be imported from the sqlalchemy.orm namespace. 


# SQLAlchemy 2.0 integration of Core API use within the ORM.

SQLAlchemy 2.0 in particular features a much greater level of integration of Core API use within the ORM.

# CORE engine vs ORM session

When using the ORM, the Engine is managed by another object called the Session. The Session in modern SQLAlchemy emphasizes a transactional and SQL execution pattern that is largely identical to that of the Connection discussed below, so while this subsection is Core-centric, all of the concepts here are essentially relevant to ORM use as well and is recommended for all ORM learners. The execution pattern used by the Connection will be contrasted with that of the Session at the end of this section.

## Getting a Connection¶

```
>>> from sqlalchemy import text
>>> with engine.connect() as conn:
...     result = conn.execute(text("select 'hello world'"))
...     print(result.all())
```

## commit as you go  vs Begin once  style



```
# "commit as you go"
>>> with engine.connect() as conn:
...     conn.execute(text("CREATE TABLE some_table (x int, y int)"))
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
...     )
...     conn.commit()
```

```
# "begin once"
>>> with engine.begin() as conn:
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
...     )
```


## What’s “BEGIN (implicit)”?


 “implicit” here means that SQLAlchemy did not actually send any command to the database; it just considers this to be the start of the DBAPI’s implicit transaction. 

 # Basics of Statement Execution

- Connection.execute()
- text()
- Result

We have seen a few examples that run SQL statements against a database, making use of a method called Connection.execute(), in conjunction with an object called text(), and returning an object called Result. In this section we’ll illustrate more closely the mechanics and interactions of these components.


# using session

```
>>> from sqlalchemy.orm import Session

>>> stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
>>> with Session(engine) as session:
...     result = session.execute(stmt, {"y": 6})
...     for row in result:
...         print(f"x: {row.x}  y: {row.y}")
```


we directly replace the call to `with engine.connect() as conn` with `with Session(engine) as session`, and then make use of the `Session.execute()` method just like we do with the `Connection.execute()` method.


## commit as you go with session

```
Also, like the Connection, the Session features “commit as you go” behavior using the Session.commit() method, illustrated below using a textual UPDATE statement to alter some of our data:

>>> with Session(engine) as session:
...     result = session.execute(
...         text("UPDATE some_table SET y=:y WHERE x=:x"),
...         [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
...     )
...     session.commit()
```

understand that `Session.execute()` method used the same way as `Connection.execute()`

# Inserting Rows using the ORM Unit of Work pattern
- https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation


When using the ORM, the Session object is responsible for constructing Insert constructs and emitting them as INSERT statements within the ongoing transaction. The way we instruct the Session to do so is by adding object entries to it; the Session then makes sure these new entries will be emitted to the database when they are needed, using a process known as a flush. The overall process used by the Session to persist objects is known as the unit of work pattern.

# Instances of Classes represent Rows

```
>>> squidward = User(name="squidward", fullname="Squidward Tentacles")
>>> krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
```

We are able to construct these objects using the names of the mapped columns as keyword arguments in the constructor. This is possible as the User class includes an automatically generated __init__() constructor that was provided by the ORM mapping so that we could create each object using column names as keys in the constructor.

-  we did not include a primary key (i.e. an entry for the id column), since we would like to make use of the auto-incrementing primary key feature of the database
- The value of the id attribute on the above objects, if we were to view it, displays itself as None:

```
>>> squidward
User(id=None, name='squidward', fullname='Squidward Tentacles')
```

The None value is provided by SQLAlchemy to indicate that the attribute has no value as of yet. SQLAlchemy-mapped attributes always return a value in Python and don’t raise AttributeError if they’re missing, when dealing with a new object that has not had a value assigned.

At the moment, our two objects above are said to be in a state called transient - they are not associated with any database state and are yet to be associated with a Session object that can generate INSERT statements for them.

# Adding objects to a Session¶

```sql
>>> session = Session(engine)
>>> session.add(squidward)
>>> session.add(krabs)
```

When this is called, the objects are in a state known as pending and have not been inserted yet:

When we have pending objects, we can see this state by looking at a collection on the Session called Session.new:

```sql
>>> session.new
IdentitySet([User(id=None, name='squidward', fullname='Squidward Tentacles'), User(id=None, name='ehkrabs', fullname='Eugene H. Krabs')])
```

# Flushing

The Session makes use of a pattern known as unit of work. This generally means it accumulates changes one at a time, but does not actually communicate them to the database until needed. This allows it to make better decisions about how SQL DML should be emitted in the transaction based on a given set of pending changes. When it does emit SQL to the database to push out the current set of changes, the process is known as a flush.

>>> session.flush()


# session.flush() is not required always

Session features a behavior known as autoflush, which we will illustrate later. It also flushes out changes whenever Session.commit() is called.

# autogenerated primary key settings

Once the rows are inserted, the two Python objects we’ve created are in a state known as persistent, 

# the session stores the map with primary key

```sql
>>> some_squidward = session.get(User, 4)
>>> some_squidward
User(id=4, name='squidward', fullname='Squidward Tentacles')
```

Session.get() method, which will return an entry from the identity map if locally present, otherwise emitting a SELECT:

```sql
>>> some_squidward is squidward
True
```

#  select using session and classes and updating  (SELECT AND UPDATE)

```sql
>>> sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
>>> sandy
User(id=2, name='sandy', fullname='Sandy Cheeks')
>>> sandy in session.dirty
True
```

As mentioned previously, a flush occurs automatically before we emit any SELECT, using a behavior known as autoflush. We can query directly for the User.fullname column from this row and we will get our updated value back:

```sql
>>> sandy_fullname = session.execute(select(User.fullname).where(User.id == 2)).scalar_one()
```

# Deleting ORM Objects using the Unit of Work pattern (GET AND DELETE)

```sql
>>> patrick = session.get(User, 3)
>>> session.delete(patrick)
>>> session.execute(select(User).where(User.name == "patrick")).first()
>>> patrick in session
False
```


# fastapi sqlachemy 2

- https://github.com/seapagan/fastapi_async_sqlalchemy2_example/blob/main/db.py

```
"""Set up the database connection and session.""" ""
from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/postgres"
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # noqa: ERA001
# Note that (as far as I can tell from the docs and searching) there is no need
# to add 'check_same_thread=False' to the sqlite connection string, as
# SQLAlchemy version 1.4+ will automatically add it for you when using SQLite.


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models.

    All other models should inherit from this class.
    """

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


async_engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """Get a database session.

    To be used for dependency injection.
    """
    async with async_session() as session, session.begin():
        yield session


async def init_models() -> None:
    """Create tables if they don't already exist.

    In a real-life example we would use Alembic to manage migrations.
    """
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # noqa: ERA001
        await conn.run_sync(Base.metadata.create_all)
```


# aysnc alchemy fastapi

- https://dev.to/akarshan/asynchronous-database-sessions-in-fastapi-with-sqlalchemy-1o7e




# sqlachemy async postgresql

- https://stackoverflow.com/questions/77641958/how-to-close-sessions-on-postgresql-with-sqlalchemy

```
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

db_engine = create_async_engine('<DATABASE_URL>', echo=False, future=True)
async_session = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.close()
```

# Connections Not Being Closed SQLAlchemy

Your session is bound to an "engine", which in turn uses a connection pool. Each time SQLAlchemy requires a connection it checks one out from the pool, and if it is done with it, it is returned to the pool but it is not closed! This is a common strategy to reduce overhead from opening/closing connections. All the options you set above have only an impact on the session, not the connection!

By default, the connections in the pool are kept open indefinitely.


# Opening and Closing a Session

The Session may be constructed on its own or by using the sessionmaker class. It typically is passed a single Engine as a source of connectivity up front. A typical use may look like:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# an Engine, which the Session will use for connection
# resources
engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/")

# create session and add objects
with Session(engine) as session:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()
```
Above, the Session is instantiated with an Engine associated with a particular database URL. It is then used in a Python context manager (i.e. with: statement) so that it is automatically closed at the end of the block; this is equivalent to calling the Session.close() method.

The call to Session.commit() is optional, and is only needed if the work we’ve done with the Session includes new data to be persisted to the database. If we were only issuing SELECT calls and did not need to write any changes, then the call to Session.commit() would be unnecessary.

Session is not attached with any model, but rather it is attached to the object of the model. You will get the attached session from the object with the help of object_session method.



# access columns

```
>>> user_table.c.name
Column('name', String(length=30), table=<user_account>)

>>> user_table.c.keys()
['id', 'name', 'fullname']
```


# add objects to session

The objects are then added to the Session using the Session.add() method. When this is called, the objects are in a state known as pending and have not been inserted yet:

```
>>> session.add(squidward)
>>> session.add(krabs)
```

When we have pending objects, we can see this state by looking at a collection on the Session called Session.new:

```
>>> session.new
IdentitySet([User(id=None, name='squidward', fullname='Squidward Tentacles'), User(id=None, name='ehkrabs', fullname='Eugene H. Krabs')])
```

# Authentication Hashing in SQLAlchemy

```
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(16), index=True)
    company_name = db.Column(db.String(128), index=True)
    first_name = db.Column(db.String(32), index=True)
    last_name = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    #below our user model, we will create our hashing functions

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

```
u = User(email="test@examplesite.com", phone_number="1111111111")
u.set_password('P@ssw0rd')
db.session.add(u)
db.session.commit()
```

```
u = User.query.filter_by(email="test@examplesite.com").first()
u.check_password('P@ssw0rd')
True
u.check_password('notherightpassword')
False
```

# generative

“Method chaining”, referred to within SQLAlchemy documentation as “generative”, is an object-oriented technique whereby the state of an object is constructed by calling methods on the object. The object features any number of methods, each of which return a new object (or in some cases the same object) with additional state added to the object.

The two SQLAlchemy objects that make the most use of method chaining are the Select object and the Query object. For example, a Select object can be assigned two expressions to its WHERE clause as well as an ORDER BY clause by calling upon the Select.where() and Select.order_by() methods:

```
stmt = (
    select(user.c.name)
    .where(user.c.id > 5)
    .where(user.c.name.like("e%"))
    .order_by(user.c.name)
)
```


# select() from a Table vs. ORM class

While the SQL generated in these examples looks the same whether we invoke select(user_table) or select(User), in the more general case they do not necessarily render the same thing, as an ORM-mapped class may be mapped to other kinds of “selectables” besides tables. The select() that’s against an ORM entity also indicates that ORM-mapped instances should be returned in a result, which is not the case when SELECTing from a Table object.

Each method call above returns a copy of the original Select object with additional qualifiers added.

# Table vs Declarative Table

```
>>> from sqlalchemy import Table, Column, Integer, String
>>> user_table = Table(
...     "user_account",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("name", String(30)),
...     Column("fullname", String),
... )
```

# declaring mapped classes

```
>>> from typing import List
>>> from typing import Optional
>>> from sqlalchemy.orm import Mapped
>>> from sqlalchemy.orm import mapped_column
>>> from sqlalchemy.orm import relationship

>>> class User(Base):
...     __tablename__ = "user_account"
...
...     id: Mapped[int] = mapped_column(primary_key=True)
...     name: Mapped[str] = mapped_column(String(30))
...     fullname: Mapped[Optional[str]]
...
...     addresses: Mapped[List["Address"]] = relationship(back_populates="user")
...
...     def __repr__(self) -> str:
...         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

>>> class Address(Base):
...     __tablename__ = "address"
...
...     id: Mapped[int] = mapped_column(primary_key=True)
...     email_address: Mapped[str]
...     user_id = mapped_column(ForeignKey("user_account.id"))
...
...     user: Mapped[User] = relationship(back_populates="addresses")
...
...     def __repr__(self) -> str:
...         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```



## Difference between SQLAlchemy Select and Query API

- https://docs.sqlalchemy.org/en/14/changelog/migration_20.html#migration-orm-usage

- https://stackoverflow.com/questions/72828293/difference-between-sqlalchemy-select-and-query-api

but in the SQLAlchemy docs they talk about introducing select() as part of the new 2.0 style for the ORM. Previously (1.x style), the query() method were used to fetch data. What is the difference between these two?

For example, for querying a Users table for a user with email and name we can do something as followed in Query API:

```
session.query(Users).filter_by(name='name', email='mail@example.com').first()
```

In Select API, the same leads to more code:

```
from sqlalchemy import select
query = select(Users).filter_by(name='name', email='mail@example.com')
user = session.execute(query).fetchone()
``` 


The biggest difference is how the select statement is constructed. The new method creates a select object which is more dynamic since it can be constructed from other select statements, without explicit subquery definition:

```
# select from a subqeuery styled query
q = select(Users).filter_by(name='name', email='mail@example.com')
q = select(Users.name, Users.email).select_from(q)
```

The outcome is more "native sql" construction of querying, as per the latest selectable API. Queries can be defined and passed throughout statements in various functionalities such as where clauses, having, select_from, intersect, union, and so on.


# Return exactly one scalar result or raise an exception.

This is equivalent to calling Result.scalars() and then Result.one().


# scalara all

This question is probably me not understanding architecture of (new) sqlalchemy, typically I use code like this:

```
query = select(models.Organization).where(
    models.Organization.organization_id == organization_id
)
result = await self.session.execute(query)

return result.scalars().all()
```

Works fine, I get a list of models (if any).

```
session.execute(
  select(User)
).scalars().all()

# or

session.scalars(
  select(User)
).all()
```

# answer

> My understanding so far was that in new sqlalchemy we should always call scalars() on the query

That is mostly true, but only for queries that return whole ORM objects. Just a regular `.execute()`

```python
    query = select(Payment)

    results = sess.execute(query).all()
    print(results)  # [(Payment(id=1),), (Payment(id=2),)]
    print(type(results[0]))  # <class 'sqlalchemy.engine.row.Row'>
```

returns a list of `Row` objects, each containing a single ORM object. Users found that awkward since they needed to unpack the ORM object from the `Row` object. So `.scalars()` is now recommended

```python
    results = sess.scalars(query).all()
    print(results)  # [Payment(id=1), Payment(id=2)]
    print(type(results[0]))  # <class '__main__.Payment'>
```

However, for queries that return individual attributes (columns) we don't want to use `.scalars()` because that will just give us one column from each row, normally the first column

```python
    query = select(
        Payment.id,
        Payment.organization_id,
        Payment.payment_type,
    )

    results = sess.scalars(query).all()
    print(results)  # [1, 2]
```

Instead, we want to use a regular `.execute()` so we can see all the columns

```python
    results = sess.execute(query).all()
    print(results)  # [(1, 123, None), (2, 234, None)]
```

Notes:

- `.scalars()` is doing the same thing in both cases: return a list containing a single (scalar) value from each row (default is index=0).

- `sess.scalars()` is the preferred construct. It is simply shorthand for `sess.execute().scalars()`.


```
(await db_session.scalars(select(UserDBModel).where(UserDBModel.id == user_id))).first()
```