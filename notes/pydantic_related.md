#  Field in pydantic

```
from uuid import uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
```

#  old pydantic

```
class MyModelPydantic(BaseModel):
    id: int
    field1: str
    field2: Optional[str]

    class Config:
        orm_mode = True
```

`Config.orm_mode = True` instructs Pydantic to allow ORM mode, which means Pydantic will automatically convert an ORM model instance to a Pydantic model instance when needed.


# Pydantic v1
from typing import Optional

class DataBaseOut(BaseModel):
    id: str
    name: str
    # type: str
    tmc_code: str
    # Set a default of None to make optional.
    organization: Optional[OrganizationOut] = None

    class Config:
        orm_mode = True

# Pydantic v2
class DataBaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    # type: str
    tmc_code: str
    organization: OrganizationOut | None = None


# pydantic 1

You would create a pydantic schema like this:

```
class CompanyAndProgramsSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    company_type_id: int
    programs: list[ProgramSchema] # Where ProgramSchema is just a simple schema for Programs
    
    class Config:
        orm_mode = True
```

If you had two SQLalchemy models (this is sqlalchemy 2 nonetheless, but same applies), that looked like this:

```
class Company(Base):
    __tablename__ = "company"
    
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    company_type_id: Mapped[int] = mapped_column(ForeignKey("company_type.id",  ondelete="SET NULL"), nullable=True)
    company_type: Mapped[CompanyType] = relationship("CompanyType", back_populates="companies")
    programs: Mapped[list["Program"]] = relationship("Program", back_populates="company")
    
    def __repr__(self):
        return f"<Company={self.name}>"

class Program(Base):
    __tablename__ = "program"
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="SET NULL"), nullable=True)
    company: Mapped[Company] = relationship("Company", back_populates="programs")
```
Assuming you used the above pydantic schema, you could return something that looked like this by simply using the Company model:

```
{
    "name": "EC",
    "company_type_id": 1,
    "programs": [
        {
            "name": "PIA24",
            "company_id": 2
        },
        {
            "name": "PIA23",
            "company_id": 2
        }
    ]
}
```



# Mastering JSON Serialization With Pydantic

- https://dzone.com/articles/mastering-json-serialization-with-pydantic

```
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    age: int
    dept: Optional[str]


user = User(id=1, name="Test user", age = 12, dept="Information Technology")
user.json() 
```


The JSON () method will return the string representation of the model data, which is

```
{"id":1,"name":"Test user","age":12,"dept":"Information Technology"}
```

The model instance also has a method dict() that returns the Python dictionary object. 

```
model = user.dict() 
model['name'] // Test user 
```


# Don’t Write Another Line of Code Until You See These Pydantic V2 Breakthrough Features

https://blog.det.life/dont-write-another-line-of-code-until-you-see-these-pydantic-v2-breakthrough-features-5cdc65e6b448


```
from app.models import User as UserDBModel
from app.schemas import UserResponse as UserResponseSchema
from sqlalchemy import select
from app.database import get_db_session
from snoop import pp
from typing import List

async for db_session in get_db_session():
    users = (await db_session.scalars(select(UserDBModel))).all()
    pp(users)
    pp(UserResponseSchema.model_validate(users[0]))
    pp(UserResponseSchema.model_validate(users[0]).json())

pp(users)
from pydantic import RootModel

# create a list of pydantic models
user_list = []
for user in users:
  user_list.append(UserResponseSchema.model_validate(user))

# create a root model
users = RootModel[List[UserResponseSchema]]

# dump as json
pp(users(user_list).model_dump_json())
```


# model_validate()

model_validate() : this is very similar to the __init__ method of the model, except it takes a dict or an object rather than keyword arguments. If the object passed cannot be validated, or if it's not a dictionary or instance of the model in question, a ValidationError will be raised.