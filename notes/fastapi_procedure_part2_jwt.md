# USER REGISTRATION

# Hashing Passwords

- https://medium.com/@kevinkoech265/jwt-authentication-in-fastapi-building-secure-apis-ce63f4164eb2

```
poetry add "passlib[bcrypt]"
```

```
╰─$ docker-compose -p fastapi_test-xyzp -f docker-compose.yaml exec webapp /bin/bash
(app) simha@923ed0a91d84:~/app$ poetry add "passlib[bcrypt]"
Using version ^1.7.4 for passlib

Updating dependencies
Resolving dependencies... (0.6s)

Package operations: 2 installs, 0 updates, 0 removals

  - Installing bcrypt (4.1.2)
  - Installing passlib (1.7.4)

Writing lock file
(app) simha@923ed0a91d84:~/app$ 
```


## Creating a utils.py file

- https://medium.com/@kevinkoech265/jwt-authentication-in-fastapi-building-secure-apis-ce63f4164eb2


```
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)
```

Breakdown of the code:

- `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")`: This creates an instance of the CryptContext class, specifying that the bcrypt hashing algorithm should be used. The deprecated="auto" parameter means that if bcrypt becomes deprecated in the future, passlib will automatically choose a more secure scheme. Cool right ??
- `def hash_pass(password: str) -> str:`: This is the function definition for the hash_pass function, which takes a plain-text password as input and returns the hashed password as a string.
- `return pwd_context.hash(password)`: Inside the hash_pass function, pwd_context.hash(password) is called to hash the input password using bcrypt. The resulting hash is then returned.



## what in update pydantic and sqlachemy 2.0+
- https://python.plainenglish.io/%EF%B8%8F-fastapi-pydantic-2-4-sqlalchemy-2-0-more-1d50d9948330

- The pydantic is using the pydantic-core now. It is written in Rust under the hood
SQLAlchemy improved typing and some other features


# Creating the Registration Endpoint
- https://www.kevsrobots.com/learn/fastapi/06_implementing_registration_and_login.html


# Pydantic Tutorial: Data Validation in Python Made Simple

- https://www.kdnuggets.com/pydantic-tutorial-data-validation-in-python-made-simple

# email validation

If you need email validation in your application, you can install the optional email-validator dependency when installing Pydantic like so:

`$ poetry add pydantic[email]`
 

Alternatively, you can run the following command to install email-validator:

`$ pip install email-validator` (not required will install pydantic[email])



```
# main.py

import json
from pydantic import BaseModel, EmailStr, ValidationError, validator

class Employee(BaseModel):
    name: str
    age: int
    email: EmailStr
    department: str
    employee_id: str

    @validator("employee_id")
     def validate_employee_id(cls, v):
         if not v.isalnum() or len(v) != 6:
             raise ValueError("Employee ID must be exactly 6 alphanumeric characters")
         return v

# Load and parse the JSON data
with open("employees.json", "r") as f:
    data = json.load(f)

# Validate each employee record
for record in data:
    try:
        employee = Employee(**record)
        print(f"Valid employee record: {employee.name}")
    except ValidationError as e:
        print(f"Invalid employee record: {record['name']}")
        print(f"Errors: {e.errors()}")
```

# INTEGRATING PYDANTIC AND SQLALCHEMY MODELS

While Pydantic models are great for input validation and serialization, SQLAlchemy models are used for database operations. In practice, you’ll often convert between these two model types.

For example, after validating user registration data with a Pydantic model, you’ll convert this data into an SQLAlchemy model before saving it to the database. Similarly, when fetching user data from the database, you’ll convert SQLAlchemy models into Pydantic models before sending them to clients.


# Generating unique IDs.

- https://dev.to/mbuthi/devops-with-fast-api-postgresql-how-to-containerize-fast-api-application-with-docker-1jdb

```
import uuid

def idgen() -> str:
    # Generate a random uuid string
    return str(uuid.uuid4().hex)
```