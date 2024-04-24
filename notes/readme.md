# FastAPI JWT Tutorial \| How to add User Authentication

```
https://www.youtube.com/watch?v=0A_GCXBCNUQ
```


# Setting up a FastAPI App with Async SQLALchemy 2.0 & Pydantic V2

```
https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308
```



# demo-fastapi-async-sqlalchemy

```
https://github.com/ThomasAitken/demo-fastapi-async-sqlalchemy/blob/main/backend/Dockerfile
```

# 10 Tips for adding SQLAlchemy to FastAPI

```
https://bitestreams.com/blog/fastapi-sqlalchemy/
```

# what is pydantic

Pydantic is an input validation library, so it should be used to validate user input in the API


# Some common problems with database connections


Database connection limit exceeded

Database connection timeout

Database connection is not closed properly

Database connection is not released properly


# django vs fastapi ORM

https://chaoticengineer.hashnode.dev/fastapi-sqlalchemy

unlike Django, FastAPI does not have an ORM built-in. It is entirely the developer's responsibility to select a suitable library and integrate it into the codebase.

Python engineers widely consider SQLAlchemy to be the most popular ORM available.

It's a legendary library that's been in use since 2006 and has been adopted by thousands of projects. In 2023, it received a major update to version 2.0. 

Similar to FastAPI, SQLAlchemy provides developers with powerful features and utilities without forcing them to use them in a specific way. Essentially, it's a versatile toolkit that empowers developers to use it however they see fit.

FastAPI and SQLAlchemy are a match made in heaven.

# creating a FastAPI backend application that utilizes SQLAlchemy 2.0 as the ORM.


- building models using Mapped and mapped_column
- defining an abstract model
- handling database session
- using the ORM
- creating a common repository class for all models
- preparing a test setup and adding tests

https://github.com/tobias-piotr/alchemist

# there are two kind of models

-  In the context of APIs, models represent what the backend expects in the request body and what it will return in the response data. 
- Database models, on the other hand, are more complex and represent the data structures stored in the database and the relationship types between them.



# sqlalchemy

Every model in SQLAlchemy starts with the DeclarativeBase class. Inheriting from it allows building database models that are compatible with Python type checkers.


# good practice to create an abstract model—Base class

It's also a good practice to create an abstract model—Base class in this case—that includes fields required in all models. These fields include the primary key, which is a unique identifier of every object. The abstract model often also stores the creation and update dates of an object, which are set automatically, when an object is created or updated. However, the Base model will be kept simple.


# sqlachemy model example


```
class Ingredient(Base):
    """Ingredient database model."""

    __tablename__ = "ingredient"

    name: orm.Mapped[str]
```

Moving on to the Ingredient model, the __tablename__ attribute specifies the name of the database table, while the name field uses the new SQLAlchemy syntax, allowing model fields to be declared with type annotations. This concise and modern approach is both powerful and advantageous for type checkers and IDEs, as it recognizes the name field as a string.

# models sqlalchemy

```
import uuid

from sqlalchemy import Column, ForeignKey, Table, orm
from sqlalchemy.dialects.postgresql import UUID


class Base(orm.DeclarativeBase):
    """Base database model."""

    pk: orm.Mapped[uuid.UUID] = orm.mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


potion_ingredient_association = Table(
    "potion_ingredient",
    Base.metadata,
    Column("potion_id", UUID(as_uuid=True), ForeignKey("potion.pk")),
    Column("ingredient_id", UUID(as_uuid=True), ForeignKey("ingredient.pk")),
)


class Ingredient(Base):
    """Ingredient database model."""

    __tablename__ = "ingredient"

    name: orm.Mapped[str]


class Potion(Base):
    """Potion database model."""

    __tablename__ = "potion"

    name: orm.Mapped[str]
    ingredients: orm.Mapped[list["Ingredient"]] = orm.relationship(
        secondary=potion_ingredient_association,
        backref="potions",
        lazy="selectin",
    )
```


# When working with a database, particularly when using SQLAlchemy, it is essential to understand the following concepts:

- dialect
- engine
- connection
- connection pool
- session



The final question mark is the connection pool. In the context of SQLAlchemy, a connection pool is a mechanism that manages a collection of database connections. It is designed to improve the performance and efficiency of database operations by reusing existing connections rather than creating new ones for each request. By reusing connections, the connection pool reduces the overhead of establishing new connections and tearing them down, resulting in improved performance.



# encode/databases   vs create_async_engine


encode/databases and create_async_engine are both tools used for asynchronous database access in Python, but they serve different purposes and have different features. Let's compare them:


encode/databases is focused on providing a simple and convenient async database interface specifically for use with FastAPI, while create_async_engine extends the capabilities of SQLAlchemy to support asynchronous operations.

encode/databases may be a better choice if you're building a FastAPI application and want a straightforward async database solution that integrates well with FastAPI.

create_async_engine may be more suitable if you're already using SQLAlchemy and want to add async support to your existing codebase, especially if you're using SQLAlchemy's ORM features extensively.


# FastAPI with async SQLAlchemy, celery and websockets

https://medium.com/@neverwalkaloner/fastapi-with-async-sqlalchemy-celery-and-websockets-1b40cd9528da


# encode/databases vs SQLAlchemy's asyncio

https://www.reddit.com/r/Python/comments/yrelvq/best_approach_for_async_sqlalchemy_in_fastapi/

The only difference I know between SQLAlchemy's asyncio session and encode/databases is that the former requires a generator that yields a database session, which will be consumed and get cleaned up per request. The latter involves creating database connection pool upon FastAPI startup event, and then a database object can be imported and used elsewhere.


I am leaning toward encode/databases because I don't really like the way that database connection must be injected in every route. I'm not against dependency injection but this also seems to be a lot repeated code (counter: maybe testing is a bit easier?)


# dataclass (python inbuilt)

```
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

```

# Usage
```
p = Point(1.0, 2.0)
print(p)  # Output: Point(x=1.0, y=2.0)
```
In this example, Point is a simple dataclass representing a point in a two-dimensional space. The @dataclass decorator automatically generates special methods like __init__ and __repr__, making it easy to create and represent instances of the Point class.



# db string

source: https://stackoverflow.com/questions/65142217/force-encode-databases-to-use-asyncpg-instead-of-psycopg2

```
DATABASE_URL = "postgresql://xxxxxxxxxxx" # database url for databases library
DATABASE_URL_SQLALCHEMY = "postgresql+asyncpg://xxxxxxxxxxx" # database url for SQLAlchemy
```

Also metadata.create_all(engine) won't work since that function don’t include an awaitable hook.

The documentation for databases clearly states, and I quote:

Note that if you are using any synchronous SQLAlchemy functions such as engine.create_all() or alembic migrations then you still have to install a synchronous DB driver: psycopg2 for PostgreSQL and pymysql for MySQL.



# Best approach for async SQLAlchemy in FastAPI

source: https://www.reddit.com/r/FastAPI/comments/pi0zdy/best_approach_for_async_sqlalchemy_in_fastapi/

Hey all!

I'm looking into how best to use SQLAlchemy with FastAPI and it looks like there are a few options:

Using traditional SQLAlchemy without async functions and relying on FastAPI's thread pool

Using the encode/databases library and forgoing SQLAlchemy's ORM

Utilizing SQLAlchemy's asyncio support which was recently added in version 1.4


Answer:

- The magic behind FastAPI using regular def functions and plain SQLAlchemy is super simple and straight forward
- The API that I run and manage uses raw SQL with databases.
- The third option is really slick too. Michael Kennedy from Talk Python teaches this in one of his courses and lets you get the best of both ORMs and async.


# declarative vs classical(imperative) declaration sqlachemy

## imperative or classical

```
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper

metadata = MetaData()

users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)

class User(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
       return "<User('%s')>" % (self.name)

mapper(User, users_table) # &lt;Mapper at 0x...; User&gt;
```

## Declarative syntax

```
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
     __tablename__ = 'users'
     id = Column(Integer, primary_key=True)
     name = Column(String)

     def __init__(self, name):
         self.name = name

     def __repr__(self):
         return "<User('%s')>" % (self.name)
```

- Answer: 
**The Django ORM is strictly declarative -- and people like that.**

- What is the benefit of using this:

```
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy import Column, Integer, String
class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     name = Column(String(16))
     fullname = Column(String(60))
     nickname = Column(String(50))
```

Instead of this:

```
from sqlalchemy import *
metadata = MetaData()
user = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(16)),
    Column('fullname ', String(60)),
    Column('nickname ', String(50))
)
```

The latter one is already a class representation, isn't it? Why are we building another class over the already existing table class? What's the benefit?


- Answer
- Some examples in the documentation still use the classical approach, but note that the classical as well as Declarative approaches are fully interchangeable.



#  main.py


```
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", log_level="info")
```

```
--app
----app.py
----db.py
----schemas.py
----users.py
```



#  asynccontextmanager


asynccontextmanager is a decorator provided by the contextlib module in Python for creating asynchronous context managers.

Context managers in Python are objects that are used with the with statement to establish and release resources or to perform setup and cleanup actions. They are typically used when you need to acquire and release resources reliably, such as opening and closing files, managing locks, or working with database connections.

In Python, context managers are created using the __enter__() and __exit__() methods for synchronous code. However, with the increasing use of asynchronous programming in Python, there's a need for asynchronous context managers that can be used with async with statements.

The asynccontextmanager decorator allows you to define asynchronous context managers using asynchronous generators. An asynchronous generator is a function that contains the async keyword in its definition and contains yield statements to produce a series of values asynchronously.


```
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_resource_manager():
    # Setup code
    print("Acquiring resource...")
    await asyncio.sleep(1)  # Simulating asynchronous setup
    
    try:
        # Resource is yielded to the caller
        yield "Resource"
    finally:
        # Cleanup code
        print("Releasing resource...")
        await asyncio.sleep(1)  # Simulating asynchronous cleanup

# Using the async context manager
async def main():
    async with async_resource_manager() as resource:
        print(f"Using {resource}...")
        # Do something with the resource asynchronously

# Running the main coroutine
import asyncio
asyncio.run(main())
```

# Asynchronous Database Sessions in FastAPI with SQLAlchemy

source: https://dev.to/akarshan/asynchronous-database-sessions-in-fastapi-with-sqlalchemy-1o7e



#  FastAPI and async SQLAlchemy 2.0 with pytest done right

## configuration file will be used to get the database connection string from the environment variables.

```python
# app/config.py
import os

class Config:
    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=os.getenv("DB_USER", "fastapi"),
            DB_PASSWORD=os.getenv("DB_PASSWORD", "fastapi-password"),
            DB_HOST=os.getenv("DB_HOST", "fastapi-postgresql:5432"),
            DB_NAME=os.getenv("DB_NAME", "fastapi"),
        ),
    )


config = Config
```

## database connection and session handling

```python
# app/services/database.py
import contextlib
from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base
```

Notice that we're importing the async versions of the SQLAlchemy classes and factories.

Then, let's create a session manager for our database. This class will be used as a singleton and will be responsible for abstracting the database connection and session handling:


# AsyncIterator


In Python, an AsyncIterator is an asynchronous iterator object that allows you to asynchronously iterate over a collection of values or asynchronously generate values.

Async iterators are designed to work with the async for statement introduced in Python 3.6 for asynchronous programming. They provide a way to asynchronously produce values one at a time, which can be useful when dealing with asynchronous operations such as fetching data from a database or making asynchronous HTTP requests.


# Coroutines and asynchronous context managers are two important concepts in asynchronous programming in Python, particularly in asyncio.


## Coroutines:

Coroutines are special types of functions that can pause and resume their execution. They are defined using the async def syntax in Python. Coroutines allow you to write asynchronous code that can perform I/O-bound operations efficiently without blocking the event loop.

```
async def my_coroutine():
    print("Start coroutine")
    await asyncio.sleep(1)  # Asynchronous sleep for 1 second
    print("Coroutine completed")
```

You can await coroutines using the await keyword within other coroutines or within an asynchronous function.



# context managers

source: https://stackoverflow.com/questions/37433157/asynchronous-context-manager

## SOLUTION 1

Here's what mine ended up looking like for anyone who want's some example code:

```python
class SMTPConnection():
    def __init__(self, url, port, username, password):
        self.client   = SMTPAsync()
        self.url      = url
        self.port     = port
        self.username = username
        self.password = password

    async def __aenter__(self):
        await self.client.connect(self.url, self.port)
        await self.client.starttls()
        await self.client.login(self.username, self.password)

        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.quit()
```

usage:

```python
async with SMTPConnection(url, port, username, password) as client:
    await client.sendmail(...)
```

Feel free to point out if I've done anything stupid.


## ANOTHER SOLUTION:


```
from contextlib import asynccontextmanager

@asynccontextmanager
async def smtp_connection():
    client = SMTPAsync()
    ...

    try:
        await client.connect(smtp_url, smtp_port)
        await client.starttls()
        await client.login(smtp_username, smtp_password)
        yield client
    finally:
        await client.quit()
```


# @asynccontextmanager  decorator vs class

The choice between using the @asynccontextmanager decorator and defining an asynchronous context manager as a class depends on your specific use case and personal preference. Both approaches achieve the same goal of creating asynchronous context managers, but they have different syntax and usage patterns.


`Usage of Generators:` It leverages Python's generator feature, where you can yield a value to temporarily transfer control to the caller and then resume execution when the caller is done with the context.

Using @asynccontextmanager Decorator:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_resource_manager():
    # Setup
    print("Acquiring resource...")
    try:
        yield "Resource"
    finally:
        # Cleanup
        print("Releasing resource...")
```
Class-based Asynchronous Context Manager:

```python
class AsyncResourceManager:
    async def __aenter__(self):
        # Setup
        print("Acquiring resource...")
        return "Resource"

    async def __aexit__(self, exc_type, exc, tb):
        # Cleanup
        print("Releasing resource...")

async def main():
    async with AsyncResourceManager() as resource:
        # Do something with the resource
        print(f"Using {resource}...")

import asyncio
asyncio.run(main())
```

# difference between


`async with session.get(url=url) as r:` 

and 

`r = await session.get(url=url)`

first form executes two special functions and the second one doesn't. The first one is somewhat equivalent to:

```
try:
    x = session.get(url=url)
    r = await x.__aenter__()    
    # the indented block of code executes here
finally:
    await x.__aexit__(...)
```


# singleton

```
class Foo(object):
     pass
```

```
some_global_variable = Foo()
```

Modules are imported only once, everything else is overthinking. Don't use singletons and try not to use globals.


Use a module. It is imported only once. Define some global variables in it - they will be singleton's 'attributes'. Add some functions - the singleton's 'methods'.

You probably never need a singleton in Python. Just define all your data and functions in a module and you have a de facto singleton:



# async generator function


 An asynchronous generator function is defined using the async def syntax, and it contains one or more yield statements to produce values asynchronously.

 Async generators are useful when you need to asynchronously generate a sequence of values, similar to regular generator functions but in an asynchronous context.


```python
from typing import AsyncGenerator

async def async_counter() -> AsyncGenerator[int, None]:
    for i in range(5):
        yield i
        await asyncio.sleep(1)
```



# annotation AsyncGenerator vs AsyncIterator


Function vs Object: AsyncGenerator is used to annotate functions that generate values asynchronously, while AsyncIterator is used to annotate objects that support asynchronous iteration.



In summary, AsyncGenerator is used for annotating asynchronous generator functions, while AsyncIterator is used for annotating objects that support asynchronous iteration. Both are essential for annotating asynchronous code involving iteration in Python.


```python
from typing import AsyncGenerator

async def async_counter() -> AsyncGenerator[int, None]:
    for i in range(5):
        yield i
        await asyncio.sleep(1)
```


vs

```python
from typing import AsyncIterator

class AsyncCounter:
    def __aiter__(self) -> AsyncIterator[int]:
        return self

    async def __anext__(self) -> int:
        if self.count < self.limit:
            value = self.count
            self.count += 1
            return value
        else:
            raise StopAsyncIteration
```


# Asynchronous Generators:  vs Asynchronous Iterators:



Asynchronous iterators and generators serve similar purposes in Python's asynchronous programming, but they operate in slightly different ways and are used in different contexts. Let's explore each:


Usage: Asynchronous generators are useful when you need to asynchronously generate a sequence of values, especially when each value involves asynchronous computation or I/O operations.

```python
async def async_counter():
    for i in range(5):
        yield i
        await asyncio.sleep(1)
```

# Using async for with asynchronous generators in Python

```python
import asyncio

async def async_counter(limit):
    for i in range(limit):
        yield i
        await asyncio.sleep(1)  # Simulate an asynchronous operation

async def main():
    async for i in async_counter(5):
        print(i)
        
await main()
```


# yeild


```python
def my_generator():
    print("First value")
    yield 1
    print("Second value")
    yield 2
    print("Last value")

gen = my_generator()  # Creates a generator object
print(next(gen))  # Prints "First value", yields 1
print(next(gen))  # Prints "Second value", yields 2
print(next(gen))  # Prints "Last value", raises StopIteration
```

Output:

```
First value
1
Second value
2
Last value
```


# example


```
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def nada():
    # await asyncio.sleep(0.0)
    yield
    
async def aloop():
    for _ in range(5):
        # await asyncio.sleep(0.0)
        yield
    
async def atask(name):
    async for _ in aloop():
        async with nada():
            print("Task", name)

async def main():
    asyncio.create_task(atask("1"))
    await asyncio.create_task(atask("2"))

if __name__ == "__main__":
    asyncio.run(main())
```


# what are generator in python

```python
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
```
Generator functions use the yield keyword to produce a sequence of values lazily, pausing and resuming execution between each yield statement.

When you iterate over a generator object using a loop, or when you call next() on it, the generator function executes until it encounters a yield statement, at which point it yields the value and pauses.

You can create a generator function that produces an infinite sequence of values by using a loop or recursion. 

```python
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

# Example usage
gen = infinite_sequence()
for _ in range(10):
    print(next(gen))
```

The infinite_sequence() generator function uses a while True loop to keep generating values indefinitely.

You can use this generator function to generate values lazily without consuming excessive memory, as it only generates values as needed. 


# asynccontextmanager with and without try block

- with try

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_resource_manager():
    # Setup code goes here
    print("Acquiring resource asynchronously...")
    try:
        yield "Resource"  # Yielding the resource to the caller
    finally:
        # Cleanup code goes here
        print("Releasing resource asynchronously...")
        
# Using the asynchronous context manager
async def main():
    async with async_resource_manager() as resource:
        print(f"Using {resource}...")
        # Do something with the resource asynchronously

import asyncio
asyncio.run(main())
```

- without try

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_resource_manager():
    # Setup code goes here
    print("Acquiring resource asynchronously...")
    yield "Resource"  # Yielding the resource to the caller
    # No explicit cleanup code is needed here

# Using the asynchronous context manager
async def main():
    async with async_resource_manager() as resource:
        print(f"Using {resource}...")
        # Do something with the resource asynchronously

import asyncio
asyncio.run(main())
```


# python annotation

```python
from typing import Union

# Function that may return an integer or None
def find_element(lst: list, target: int) -> Union[int, None]:
    for i, item in enumerate(lst):
        if item == target:
            return i
    return None  # If the target is not found, return None

# Function that explicitly returns nothing
def print_message(message: str) -> None:
    print(message)
```

```python
# Annotating a function that may return either an int or None using the pipe symbol
def find_element(lst: list, target: int) -> int | None:
    for i, item in enumerate(lst):
        if item == target:
            return i
    return None  # If the target is not found, return None
```



# factory methods

- In Python, factory methods are used to create objects.
- They are often implemented as class methods within a class.

- The purpose of factory methods is to abstract the process of object creation and provide flexibility in creating instances of different classes or subclasses.

- Factory methods are useful in scenarios where the creation of objects involves complex logic, or where the exact class of the object to be created may vary dynamically based on runtime conditions or configurations. They encapsulate the object creation process and promote loose coupling between the client code and the classes being instantiated.


```python
class Shape:
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print("Drawing a circle")

class Rectangle(Shape):
    def draw(self):
        print("Drawing a rectangle")

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type):
        if shape_type == 'circle':
            return Circle()
        elif shape_type == 'rectangle':
            return Rectangle()
        else:
            raise ValueError("Invalid shape type")

# Usage
circle = ShapeFactory.create_shape('circle')
rectangle = ShapeFactory.create_shape('rectangle')

circle.draw()     # Output: Drawing a circle
rectangle.draw()  # Output: Drawing a rectangle
```


#  sqlalchemy

```python
postgresql+asyncpg://<db_username>:<db_secret>@<db_host>:<db_port>/<db_name>
```


```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    <your_connection_string>,
    echo=True,
    future=True,
)
```

# session for every request

In web applications, it's common to create a new SQLAlchemy session for every request. This ensures that each request operates within its own transactional context and allows for proper management of database connections and resources.

To achieve this pattern, you typically use a web framework such as Flask or FastAPI, along with middleware or request lifecycle hooks to manage session creation and teardown.

In a FastAPI application, you can achieve creating a SQLAlchemy session for every request using middleware or dependency injection. One common approach is to use FastAPI's dependency injection system to create and manage sessions.


# fastapi session maker

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Create the SQLAlchemy engine
DATABASE_URL = "sqlite:///./example.db"
engine = create_engine(DATABASE_URL)

# Create a sessionmaker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a function to get a new session for every request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app instance
app = FastAPI()

# Define a route that uses the session
@app.get("/")
async def read_root(db: Session = Depends(get_db)):
    # Perform database operations within the request
    return {"message": "Hello, World!"}
```

# When you use Depends with a function that contains a yield statement

In FastAPI, Depends is a powerful tool for handling dependencies and injecting them into route handler functions. When you use Depends with a function that contains a yield statement, FastAPI treats it as a coroutine function and automatically awaits its execution before injecting the dependency into the route handler.

Here's an example demonstrating how Depends works with a dependency function containing yield:

```python
from fastapi import Depends, FastAPI

app = FastAPI()

# Dependency function with yield
async def get_dependency():
    print("Preparing dependency...")
    yield "This is the dependency"
    print("Dependency cleanup...")

# Route handler function with dependency injection
@app.get("/")
async def read_root(dep: str = Depends(get_dependency)):
    return {"message": dep}
```
In this example:

- We define a dependency function get_dependency() with an asynchronous generator. It prints a message when preparing the dependency and cleaning up afterward.
- We use Depends(get_dependency) to specify that the read_root route handler function depends on the result of get_dependency.
- When a request comes in, FastAPI executes get_dependency(), awaits its result, and injects the value into the dep parameter of the read_root route handler function.
- FastAPI automatically handles the cleanup of the dependency after the request completes.

This pattern allows you to perform any necessary setup or cleanup logic before and after handling each request, providing a flexible way to manage dependencies in your FastAPI application.


```python
from fastapi import Depends, FastAPI

app = FastAPI()

# Synchronous dependency function
def get_dependency():
    return "This is a dependency"

# Route handler function with dependency injection
@app.get("/")
async def read_root(dep: str = Depends(get_dependency)):
    return {"message": dep}
```


# fastapai sqlachemy async session


To use an async SQLAlchemy session in a FastAPI application, you can create a dependency that manages the session creation and cleanup. This allows you to have a new session for each request and ensures that the session is properly closed after the request completes. Here's how you can achieve this:

```PYTHON
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Create the async SQLAlchemy engine
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a sessionmaker bound to the engine
async_sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency function to create async session
async def get_db():
    async with async_sessionmaker() as session:
        yield session

app = FastAPI()

# Route handler function with dependency injection
@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        # Perform database operations within the request
        result = await db.execute("SELECT * FROM my_table")
        data = result.fetchall()
        return {"data": data}
```



# sqlaclhemy session

source: https://chaoticengineer.hashnode.dev/fastapi-sqlalchemy

```python
from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from alchemist.config import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.DATABASE_URL)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise
```


# sqlachemy create SQLAlchemy engine and sessionmaker globally

- Initialization: Initialize your SQLAlchemy engine and sessionmaker globally when the FastAPI application starts up.
- Dependency Injection: Use FastAPI's dependency injection system to create a dependency that provides a new session for each request.
- Scope: Ensure that each request gets its own session and that sessions are properly closed after the request completes.

```python
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Initialize the SQLAlchemy engine globally
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

# Create a sessionmaker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app instance
app = FastAPI()

# Dependency function to get a new session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route handler function with dependency injection
@app.get("/")
async def read_root(db: Session = Depends(get_db)):
    # Use the session to perform database operations
    ...

# Close the engine when the application shuts down
@app.on_event("shutdown")
def shutdown_event():
    engine.dispose()
```


# Asynchronous SQLAlchemy:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Define the async engine and session
async_engine = create_async_engine('sqlite+aiosqlite:///test.db', echo=True)
async_sessionmaker = sessionmaker(async_engine, class_=AsyncSession)

# Define an asynchronous ORM model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Perform database operations asynchronously
async_session = async_sessionmaker()
user = User(name='John')
async with async_session.begin():
    async_session.add(user)
```


# FastAPI, SQLAlchemy, and Parallel Queries Walk Into a Bar…

https://medium.com/@lironbenyeda/fastapi-sqlalchemy-and-parallel-queries-walk-into-a-bar-86dfe40aa878

# execute parallel queries

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

app = FastAPI()

# Dependency function to get async session
async def get_db():
    async with AsyncSession() as session:
        yield session

# Asynchronous function to execute SQL statement 1
async def sql_statement_1(db: AsyncSession):
    result = await db.execute(select(...))  # Replace select(...) with your SQL statement
    return result.fetchall()

# Asynchronous function to execute SQL statement 2
async def sql_statement_2(db: AsyncSession):
    result = await db.execute(select(...))  # Replace select(...) with your SQL statement
    return result.fetchall()

# Asynchronous function to execute SQL statement 3
async def sql_statement_3(db: AsyncSession):
    result = await db.execute(select(...))  # Replace select(...) with your SQL statement
    return result.fetchall()

@app.get("/")
async def parallel_sql_statements(db: AsyncSession = Depends(get_db)):
    # Execute multiple SQL statements concurrently
    result_1, result_2, result_3 = await asyncio.gather(
        sql_statement_1(db),
        sql_statement_2(db),
        sql_statement_3(db)
    )

    return {"result_1": result_1, "result_2": result_2, "result_3": result_3}
```


# dependency injection yeild vs return


Here's a comparison between the two approaches:

## yield


```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## return

```python
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
```



# async-fastapi-sqlalchemy 

https://github.com/rhoboro/async-fastapi-sqlalchemy

# FastAPI-boilerplate

https://github.com/igorbenav/FastAPI-boilerplate


# The ultimate async setup: FastAPI, SQLModel, Alembic, Pytest

https://medium.com/@estretyakov/the-ultimate-async-setup-fastapi-sqlmodel-alembic-pytest-ae5cdcfed3d4

https://github.com/ETretyakov/hero-app




# 3- Your First FastApi+JWT token

https://dev.to/sambo2021/3-your-first-fastapijwt-token-3fi4

https://github.com/sambo2021/python-dev/tree/master/fastapi-auth-project

# pip install "passlib[bcrypt]"

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)
if __name__ == "__main__":
    print(hash_password("adrian123"))
```

`pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto"): `

This creates an instance of the CryptContext class, specifying that the `bcrypt` hashing algorithm should be used.
The `deprecated="auto"` parameter means that if `bcrypt` becomes deprecated in the future, `passlib` will automatically choose a more secure scheme.


## OAuth2 with Password and Bearer:




# alembic naming convention


Here is a block of code you should never forget when you’re building your database schemas with SQLAlchemy & Alembic:

```
convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
```

for sqlmodel

```
from sqlmodel import Field, SQLModel

metadata = SQLModel.metadata

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = SQLModel.metadata
metadata.naming_convention = NAMING_CONVENTION
```


If you have not used this block of code (or a portion of it), you most likely have run into some issues, such as not being able to drop a constraint. This is because the operation Operations.drop_constraint() needs to know the name of the constraint.


When we define the models using a MetaData like such, the naming convention dictionary would provide names for all our constraints and indexes. With this approach, you ensure consistency and predictability in your database schema. All your constraints and indexes will have meaningful and structured names based on the defined convention. 




# type hints cheat sheet

https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html


# Python Types Intro

Python has support for optional "type hints" (also called "type annotations").

These "type hints" or annotations are a special syntax that allow declaring the type of a variable.

By declaring types for your variables, editors and tools can give you better support.



# async_sessionmaker with sqlalchemy


```python
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    f"mysql+asyncmy://{_db_user}:{_db_passwd}@{_db_host}:{_db_port}/{_db_schema}",
    echo=False,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async with async_session() as session:
   result = await session.execute(text(query))
   result = result.mappings().fetchall()
```


# sqlmodel and async

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel
from typing import Optional

user = "user"
password = "password"
host = "db"
db = "db"
engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{db}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        yield session


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    content: str = Field()
    


## Endpoint for delete
from fastapi import FastAPI, Depends
from sqlalchemy import select, update
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from database import Item, get_db
import logging

app = FastAPI()

async def get_item(item_id: int, db: AsyncSession):
    query = select(Item).where(Item.id == item_id).options(selectinload('*'))
    result = await db.exec(query)
    return result.first()

@app.delete("item/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    await db.delete(await get_item(item_id, db))
    await db.commit()
    return await get_all(db)
```


# async and sqlmodel

https://dev.to/arunanshub/async-database-operations-with-sqlmodel-c2o

1. Install an async-powered database engine (like, aiosqlite, asyncpg etc.)
```bash
poetry add aiosqlite
```
2. Set up a database URL that includes the name of the async database engine.
```python
>>> DATABASE_URL = "sqlite+aiosqlite:///path/to/database.db"
>>> # Note the use of aiosqlite
```
3. Create a database engine with sqlalchemy.ext.asyncio.create_async_engine().
```python
>>> from sqlalchemy.ext.asyncio import create_async_engine
>>> engine = create_async_engine(DATABASE_URL)
```
4. Use the engine to create a database session using sqlmodel.ext.asyncio.session.AsyncSession.
```python
>>> from sqlmodel.ext.asyncio.session import AsyncSession
>>> async with AsyncSession(engine) as session:
...     # perform database operations
Use the session to perform database operations.
>>> async with AsyncSession(engine) as session:
...     db_user = models.User(name="chonk")
...     session.add(db_user)
...     await session.commit()
...     await session.refresh(db_user)
>>> print(db_user.id)
2
```


# with and without

## Create Async Engine

```python
# sqlmodel_alembic_async/databases.py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./data.db"

engine = create_async_engine(DATABASE_URL, echo=True)
```

# Create Async Session

```python
>>> from sqlmodel.ext.asyncio.session import AsyncSession
>>> from sqlmodel_alembic_async.databases import engine
>>>
>>> session = AsyncSession(engine)

## without 

Now, we just have to create the model objects. We created the model objects in part 1.

>>> # ...
>>> from sqlmodel_alembic_async.models import User, Pet
>>> user_chonky = User(name="chonky")
>>> pet_frog = Pet(name="phroge")

We add our object to the session and commit to the database using session.commit().

>>> # ...
>>> # Use the session to perform database operations
>>> session.add_all((user_chonky, pet_tiger))
>>> await session.commit()


SQLAlchemy is logging its operations since we passed echo=True to create_async_engine.

Once committed, the objects must be refreshed with session.refresh().

>>> # ...
>>> await session.refresh(user_chonky)
INFO sqlalchemy.engine.Engine BEGIN (implicit)
INFO sqlalchemy.engine.Engine SELECT user.name, user.id
FROM user 
WHERE user.id = ?
INFO sqlalchemy.engine.Engine [generated in 0.00016s] (3,)
>>>
>>> await session.refresh(pet_tiger)
INFO sqlalchemy.engine.Engine SELECT pet.id, pet.name 
FROM pet 
WHERE pet.id = ?
INFO sqlalchemy.engine.Engine [generated in 0.00018s] (2,)

Let"'"s inspect our model objects:
>>> # ...
>>> print(user_chonky)
User(id=3, name="chonky")
>>> print(pet_frog)
Pet(id=2, name="phroge")

And once you"'"re done with it, you can close the session.
>>> # ...
>>> await session.close()
INFO sqlalchemy.engine.Engine ROLLBACK


You can also use the session object as an async context manager like this:


>>> async with AsyncSession(engine) as session:
...     db_user = models.User(name="chonk")
...     session.add(db_user)
...     await session.commit()
...     await session.refresh(db_user)
...     # perform some other operation
```


# Working with Asyncio and SQLAlchemy

Now that we have seen how to work with SQLAlchemy, let’s explore how to use asyncio with SQLAlchemy. To query the users we can use the following code:

```python
import asyncio
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

meta = MetaData()


async def main():
    engine = create_async_engine('postgresql+asyncpg://user:password@host:port/database')
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    async with AsyncSession(engine) as session:
        async with session.begin():
            # Create a new user
            new_user = User(name='John Doe', email='john@gmail.com')
            session.add(new_user)

        # Query all users
        async with session.begin():
            users = await session.execute(select(User))
            async for user in users:
                print(user.name, user.email)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```


# AsyncSession and async with session.begin()(above):

```
async def create_postgresql_engine():
    engine =  create_async_engine(ConnectionString, future=True, echo=True)
    return engine


async def run_stmt(stmt, engine):
    df = pd.DataFrame()
    async with AsyncSession(engine) as session:
        try:
            result = await session.execute(stmt)
            rows =  result.fetchall()
            columns = result.keys()
            if len(rows) > 0:
                df = pd.DataFrame(rows, columns=columns)
            else:
                df = pd.DataFrame(columns=columns)
            df = df.rename(columns=str.lower)
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e
        else:
            await session.commit()
        finally:
            await session.close()
            await engine.dispose()

    return df
```


#  pydantic settings


Then, when you create an instance of that Settings class (in this case, in the settings object), Pydantic will read the environment variables in a case-insensitive way, so, an upper-case variable APP_NAME will still be read for the attribute app_name.



#  dbeaver as web app

https://medium.com/@kharvinagaraj1/rapidly-run-deploy-a-containerized-sql-database-and-connect-with-ease-using-a-containerized-dbeaver-ae7bcc069c3b



# Waiting for PostgreSQL to be "healthy"

https://github.com/peter-evans/docker-compose-healthcheck

A particularly common use case is a service that depends on a database, such as PostgreSQL. We can configure docker-compose to wait for the PostgreSQL container to startup and be ready to accept requests before continuing.

The following healthcheck has been configured to periodically check if PostgreSQL is ready using the pg_isready command. See the documentation for the pg_isready command here.

```
healthcheck:
  test: ["CMD-SHELL", "pg_isready"]
  interval: 10s
  timeout: 5s
  retries: 5
```



# alembic, slqModel

Alembic and SQLModel are powerful tools in the Python ecosystem for database management and ORM (Object Relational Mapping). 

poetry shell

```
poetry add alembic
poetry add sqlmodel
```


SQLModel is based on Pydantic and keeps the same design, syntax, and ideas.

Underneath, ✨ a SQLModel model is also a Pydantic model. ✨

That means you get all of Pydantic's features, including automatic data validation, serialization, and documentation. You can use SQLModel in the same way you can use Pydantic.

You can even create SQLModel models that do not represent SQL tables. In that case, they would be the same as Pydantic models.

This is useful, in particular, because now you can create a SQL database model that inherits from another non-SQL model. You can use that to reduce code duplication a lot. It will also make your code more consistent, improve editor support, etc.

This makes it the perfect combination for working with SQL databases in FastAPI applications.



# folder structure sqlModel

## Single Module for Models¶

But in this first case, all the models would live in a single file.

The file structure of the project could be:


.
├── project
    ├── __init__.py
    ├── app.py
    ├── database.py
    └── models.py


This way, you wouldn't have to deal with circular imports for other models.

And then you could import the models from this file/module in any other file/module in your application.


# fastapi, alembic, pydantic, 

https://dev.to/nehrup/fastapi-deep-dive-exploring-postgresql-sqlmodel-alembic-and-jwt-integration-foundations-2h3n


poetry add psycopg2-binary  (needed for alembic)




# psycopg  vs psycopg2-binary

Psycopg 3 is a modern implementation of a PostgreSQL adapter for Python.

Installation
Quick version:

pip install --upgrade pip               # upgrade pip to at least 20.3
pip install "psycopg[binary,pool]"      # install binary dependencies



# fastapi-alembic-sqlmodel-async


https://github.com/jonra1993/fastapi-alembic-sqlmodel-async



# fastapi-sqlalchemy-asyncpg

https://github.com/grillazz/fastapi-sqlalchemy-asyncpg/tree/main




#  postgresql async

https://medium.com/@estretyakov/the-ultimate-async-setup-fastapi-sqlmodel-alembic-pytest-ae5cdcfed3d4

In this case the database connection string for the app will look like this:

```
postgresql+asyncpg://hero:heroPass123@0.0.0.0:5432/heroes_db
```

Environment variables

We are going to use Pydantic approach to set environment variables for the project. Let’s create an .env file under the root of the project.

```
# BASE
API_V1_PREFIX="/api/v1"
DEBUG=True
PROJECT_NAME="Heroes App (local)"
VERSION="0.1.0"
DESCRIPTION="The API for Heroes app."
# DATABASE
DB_ASYNC_CONNECTION_STR="postgresql+asyncpg://hero:heroPass123@0.0.0.0:5432/heroes_db"
```

To read these variables I create a config.py (app/core/config.py) with Settings declaration. The content of config.py looks like this:

```
from pydantic import BaseSettings


class Settings(BaseSettings):
   # Base
   api_v1_prefix: str
   debug: bool
   project_name: str
   version: str
   description: str

   # Database
   db_async_connection_str: str
```

The loading of the file should be on the application initialisation, so place further code lines

```
from os import getenv

from dotenv import load_dotenv

from app.core.config import Settings

load_dotenv(getenv("ENV_FILE"))

settings = Settings()
```




# sqlachemy 


```
from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine("postgresql+psycopg2://myuser:mypassword@0.0.0.0:5432/mydb")


def app():
    with engine.connect() as conn:
        stmt = text("select * from pg_database")
        print(conn.execute(stmt).fetchall())


if __name__ == "__main__":
    app()
```


# sqlachemy model

```
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata
```


# To check if Alembic is working well run the command alembic current.

