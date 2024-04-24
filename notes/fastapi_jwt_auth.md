- https://www.freecodecamp.org/news/how-to-add-jwt-authentication-in-fastapi/


# python pydantic email

```
Since we're using an email validator, EmailStr, install email-validator:

(venv)$ pip install "pydantic[email]"
```


#  pydantic models

```
# app/model.py

class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }
```


# How do we implement hashing in your project then?

```
poetry add "passlib[bcrypt]"
```

# Creating a utils.py file

```
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password:str):
    return pwd_context.hash(password)
```

- pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto"): This creates an instance of the CryptContext class, specifying that the bcrypt hashing algorithm should be used. The deprecated="auto" parameter means that if bcrypt becomes deprecated in the future, passlib will automatically choose a more secure scheme. Cool right ??


# APIROUTER

Let's say the file dedicated to handling just users is the submodule at /app/routers/users.py.


# post request

- It then checks to make sure another account with the email/username does not exist. Then it creates the user and saves it to the database.

```
@router.post('/', status_code=status.HTTP_201_CREATED,response_model=schemas.UserOutput)
def create_users(user:schemas.CreateUser, db:Session = Depends(get_db)):

    # Hash The Password
    hashed_pass = hash_pass(user.password)

    user.password = hashed_pass

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
```


# pydantic schemas

```
from pydantic import BaseModel, Field, EmailStr

class UserBaseSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str



class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")
```


# ORM and pydantic

```
return UserResponse.from_orm(user)
```

# get user from email


## Difference between SQLAlchemy Select and Query API

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


# signup

```python
from fastapi import APIRouter, status, HTTPException
import app.schemas as schemas
from app.dependencies.core import DBSessionDep
from app.crud.user import get_user_by_email, create_user
from app.utils import hash_pass

router = APIRouter(
        prefix="/users",
        tags=["users"],
    )

@router.post('/signup', summary="Create new user", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
async def create_users(user_payload:schemas.UserCreate, db_session:DBSessionDep):
    # querying database to check if user already exist
    user = await get_user_by_email(db_session, user_payload.email)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    # Hash The Password
    user_payload.hashed_password = hash_pass(user_payload.hashed_password)

    new_user = await create_user(db_session, user_payload)
    return new_user

```

Schema

```python
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    hashed_password: str = Field(alias="password")

class UserResponse(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    id: int
    disabled: bool
    model_config = ConfigDict(from_attributes=True)
```

dbModel

```python
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)
```

check user exists

```python
async def get_user_by_email(db_session: AsyncSession, email: str):
    return (await db_session.scalars(select(UserDBModel).where(UserDBModel.email == email))).first()

async def create_user(db_session: AsyncSession, user:UserCreate):
    db_user = UserDBModel(**user.dict())
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user
```

Note we used alias password for hased_password but it will be accessed only as hashed_password

# How to Handle Logins

- https://www.freecodecamp.org/news/how-to-add-jwt-authentication-in-fastapi/

How to Handle Logins
FastAPI has a standard way of handling logins to comply with OpenAPI standards. This automatically adds authentication in the swagger docs without any extra configurations.

Add the following handler function for user logins and assign each user access and refresh tokens. Don't forget to include imports.

This endpoint is a bit different from the other post endpoints where you defined the schema for filtering incoming data.

For login endpoints, we use OAuth2PasswordRequestForm as a dependency. This will make sure to extract data from the request and pass is as a form_data argument to the the login handler function. python-multipart is used to extract form data. So make sure that you have installed it.


# get secret key

```
openssl rand -hex 32
```


# OAuth2PasswordBearer

First install python-multipart.

E.g. poetry install python-multipart

This is because OAuth2 uses "form data" for sending the username and password.

use OAuth2, with the Password flow, using a Bearer token. We do that using the OAuth2PasswordBearer class.


When we create an instance of the OAuth2PasswordBearer class we pass in the tokenUrl parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the username and password in order to get a token.


```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

Here tokenUrl="token" refers to a relative URL token that we haven't created yet. As it's a relative URL, it's equivalent to ./token.

Because we are using a relative URL, if your API was located at https://example.com/, then it would refer to https://example.com/token. But if your API was located at https://example.com/api/v1/, then it would refer to https://example.com/api/v1/token.


This parameter doesn't create that endpoint / path operation, but declares that the URL /token will be the one that the client should use to get the token. That information is used in OpenAPI, and then in the interactive API documentation systems.

The oauth2_scheme variable is an instance of OAuth2PasswordBearer, but it is also a "callable".

It could be called as:

`oauth2_scheme(some, parameters)`

So, it can be used with **Depends**.

Now you can pass that oauth2_scheme in a dependency with Depends.

This dependency will provide a str that is assigned to the parameter token of the path operation function.

FastAPI will know that it can use this dependency to define a "security scheme" in the OpenAPI schema (and the automatic API docs).

# for jwt install

poetry install python-jose[cryptography]


# Using a DB dependency in FastAPI without having to pass it through a function tree #2894

-- https://github.com/tiangolo/fastapi/issues/2894

I am currently working on a POC using FastAPI on a bigger application. While everything works, I've gotten some push-back from some members of my team regarding the approach of handling database sessions through dependency injection of the Session through yield. The biggest issue being mainly having to pass the Session from the controller, to a service, to a second service and (in a few cases), a third service further in. In those cases, the intermediary service functions tend to have no database queries but the functions that they call on other services might have some. The complaint mainly lies in this being more difficult to maintain and having to pass the DB object everywhere seeming uselessly repetitive.

https://stackoverflow.com/questions/66464098/using-a-db-dependency-in-fastapi-without-having-to-pass-it-through-a-function-tr


https://www.reddit.com/r/Python/comments/z45uz6/comment/ixq2dh3/


# https://github.com/jonra1993/fastapi-alembic-sqlmodel-async

from fastapi_async_sqlalchemy import db

# Add tutorial for ContextVar based DB session access from a single place #5489

https://github.com/tiangolo/fastapi/pull/5489