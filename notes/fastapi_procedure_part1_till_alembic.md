# fastapi project procedure

1) create docker compose file with 
    - postgresql service, (monut pgdata)
    - dbeaver service,  (mount dbeaver realted)  (db.localhost:8028  (add to /etc/hosts) login: gauranga, pass: K*@.8)
    - web app service which mounts project folder with 
        - Dockerfile of python 3.12 and poetry
        - gitignore
        - dockerignore
    - nginx service

# create project folder

```
- backend_fastapi
    - .gitignore
    - Dockerfile
    - .dockerignore
```

## .gitignore
```
.venv
.env
venv
*.pyc
__pycache__
Pipfile.lock
```

## .dockerignore
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
.venv
venv
*.cover
*.log
```
## Dockerfile and dockercompose files in the last

## fastapi hello world

2)  get into the webapp service (without any deps) and setup some things

```
docker-compose -p fastapi_test-xyzp run --rm --no-deps webapp /bin/bash

# setup poetry

poetry init (which will create )

# add packages
poetry add fastapi
```

3) Create folder app as follows

```
app
├── main.py
├── __init__.py
```

trying to use same structure as `https://github.com/tiangolo/full-stack-fastapi-template/tree/master/backend`


4) put the fastapi code there

```
# app/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def app_get():
    return {'info': "FastAPI Working"}
```

5) try to run the whole docker-compose up

```
docker-compose -p fastapi_test-xyzp -f docker-compose.yaml up --build --force-recreate --remove-orphans
```

6) check the api is working at

`localhost:8028`


## env variables using pydantic settings


### install

`poetry add pydantic pydantic-settings`

```
╰─$ docker-compose -p fastapi_test-xyzp -f docker-compose.yaml exec webapp /bin/bash
simha@923ed0a91d84:~/app$ poetry shell
Spawning shell within /home/simha/app/.venv
simha@923ed0a91d84:~/app$ . /home/simha/app/.venv/bin/activate
(app) simha@923ed0a91d84:~/app$ poetry add pydantic pydantic-settings
Using version ^2.7.1 for pydantic
Using version ^2.2.1 for pydantic-settings

Updating dependencies
Resolving dependencies... (3.0s)

Package operations: 2 installs, 0 updates, 0 removals

  - Installing python-dotenv (1.0.1)
  - Installing pydantic-settings (2.2.1)

Writing lock file
(app) simha@923ed0a91d84:~/app$ 
```

create a folder core and config inside


```
├── app
│   ├── core  <----------------- CREATE THIS FOLDER AND FILE WITHIN
│   │   ├── config.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py
├── Dockerfile
├── poetry.lock
└── pyproject.toml
```


add the pydantic settings inside

```
import os

from pydantic import PostgresDsn, RedisDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB_NAME: str
    POSTGRES_PORT: int = 5432

    @computed_field # type: ignore[misc]
    @property
    def asyncpg_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for asyncpg.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgresql+asyncpg".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL for asyncpg.
        """
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DB_NAME,
            port=self.POSTGRES_PORT,
        )


settings = Settings() # type: ignore[misc]
```

import as

```
from app.core.config import settings as global_settings
```

## sqlmode, alembic and asycnpg

### install asyncpg

```
poetry add asyncpg
```

```
╰─$ docker-compose -p fastapi_test-xyzp -f docker-compose.yaml exec webapp /bin/bash
simha@923ed0a91d84:~/app$ alembic init -t async alembic_migrations
bash: alembic: command not found
simha@923ed0a91d84:~/app$ poetry add asyncpg
Using version ^0.29.0 for asyncpg

Updating dependencies
Resolving dependencies... (0.1s)

Package operations: 1 install, 0 updates, 0 removals

  - Installing asyncpg (0.29.0)

Writing lock file
simha@923ed0a91d84:~/app$
```


### install sqlachemy and create a model

```
poetry add SQLAlchemy
```

```
(app) simha@923ed0a91d84:~/app$ docker-compose -p fastapi_test-xyzp -f docker-compose.yaml exec webapp /bin/bash^C
(app) simha@923ed0a91d84:~/app$ poetry add SQLAlchemy
Using version ^2.0.29 for sqlalchemy

Updating dependencies
Resolving dependencies... (0.1s)

No dependencies to install or update

Writing lock file
```

### defining SQL models with nameing convention
- https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308
- https://github.com/ThomasAitken/demo-fastapi-async-sqlalchemy

`app/models.py`


### moving to sqlalchemy 2.0 style

this is described in the upgrade guide for those moving to fully 2.0 style.
- https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#step-one-orm-declarative-base-is-superseded-by-orm-declarativebase
- pep-484 compliance.
- pep-484 typing does not support functions that return classes where those classes would be meaningful as a base class, so 1.4's typing only supported declarative_base() when the mypy plugin were used, which doesn't work with vscode. So overall there was never any supported behavior for declarative_base() without the mypy plugin being used,

### Step one - declarative_base() is superseded by DeclarativeBase.¶
One observed limitation in Python typing is that there seems to be no ability to have a class dynamically generated from a function which then is understood by typing tools as a base for new classes. To solve this problem without plugins, the usual call to declarative_base() can be replaced with using the DeclarativeBase class, which produces the same Base object as usual, except that typing tools understand it:
    

### Step two - replace Declarative use of Column with mapped_column()
The mapped_column() is an ORM-typing aware construct that can be swapped directly for the use of Column.

### Step three - apply exact Python types as needed using Mapped.
This can be done for all attributes for which exact typing is desired; attributes that are fine being left as Any may be skipped.

- At this point, our ORM mapping is fully typed and will produce exact-typed select(), Query and Result constructs. 

### creating sqlalchemy model and adding naming convention

create database.py

```
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

class Base(DeclarativeBase):
    metadata=meta
```


```
from database import Base
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    slug: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
```

model is taken from: https://github.com/ThomasAitken/demo-fastapi-async-sqlalchemy/blob/main/backend/app/models/user.py

https://medium.com/@estretyakov/the-ultimate-async-setup-fastapi-sqlmodel-alembic-pytest-ae5cdcfed3d4

As pointed out in The Importance of Naming Constraints from the Alembic docs, drop_constraint will need a name to reference

**Note**: in alembic we have to import this Base and use as Base.metadata


### Using Asyncio with Alembic

https://www.aritro.in/post/local-development-environment-with-fast-api-sqlmodel-sqlite-alembic-sync-async-version/

install `poetry add alembic`


https://testdriven.io/blog/fastapi-sqlmodel/

New configurations can use the template “async” to bootstrap an environment which can be used with async DBAPI like asyncpg, running the command:

```
alembic init -t async <script_directory_here>
```

We'll use the async template for this:

`$ alembic init -t async alembic_migrations`

This will create the alembic directory with the alembic configuration. We'll need to make a few changes to the configuration.

```
╰─$ docker-compose -p fastapi_test-xyzp -f docker-compose.yaml exec webapp /bin/bash
simha@923ed0a91d84:~/app$ poetry add alembic
The following packages are already present in the pyproject.toml and will be skipped:

  - alembic

If you want to update it to the latest compatible version, you can use `poetry update package`.
If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.

Nothing to add.
simha@923ed0a91d84:~/app$ poetry shell
Spawning shell within /home/simha/app/.venv
simha@923ed0a91d84:~/app$ . /home/simha/app/.venv/bin/activate
(app) simha@923ed0a91d84:~/app$ alembic init -t async alembic_migrations
  Creating directory '/home/simha/app/alembic_migrations' ...  done
  Creating directory '/home/simha/app/alembic_migrations/versions' ...  done
  Generating /home/simha/app/alembic_migrations/env.py ...  done
  Generating /home/simha/app/alembic_migrations/README ...  done
  Generating /home/simha/app/alembic.ini ...  done
  Generating /home/simha/app/alembic_migrations/script.py.mako ...  done
  Please edit configuration/connection/logging settings in '/home/simha/app/alembic.ini' before proceeding.
(app) simha@923ed0a91d84:~/app$ mv alembic_migrations/ app/
(app) simha@923ed0a91d84:~/app$ 
```

### Note in the above we have moved the alembic_migrations to app folder

```
mv alembic_migrations/ app/
```

### Update the path in the `alembic.ini`

```
[alembic]
# path to migration scripts
script_location = app/alembic_migrations
```

### replace sqlalchemy.url in alembic.ini (not needed we will get url from env variable)
replace sqlalchemy.url = driver://user:pass@localhost/dbname in alembic.ini with sqlite+aiosqlite:///database.db.

## alembic env.py

```
from app.core.config import settings  # <---- ADD THIS
# define models folder with __init__.py and below is not needed. enture in the __init__.py import the models
from app.models import Base

# from app.models import *  # noqa: F403 <--- ADD THIS (not needed)
# from app.database import Base # <--- ADD THIS

db_url = str(settings.asyncpg_url)  # <--------ADD THIS
config.set_main_option("sqlalchemy.url", db_url)  # <-------- ADD THIS

target_metadata = Base.metadata   # <---- MODIFY THIS
```

## alembic current

```
# first start the docker compose
$ docker-compose -p fastapi_test-xyzp -f docker-compose.yaml up --build --force-recreate --remove-orphans

# enter into webapp
╰─$ docker-compose -p fastapi_test-xyzp -f docker-compose.yaml exec webapp /bin/bash
simha@923ed0a91d84:~/app$ poetry shell
Spawning shell within /home/simha/app/.venv
simha@923ed0a91d84:~/app$ . /home/simha/app/.venv/bin/activate
(app) simha@923ed0a91d84:~/app$ alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
(app) simha@923ed0a91d84:~/app$ 

```

## alembic autogenerate

Now the autogeneration command can be run. Once it is executed, Alembic will generate a new migration script with the necessary changes based on the comparison between the database and the table metadata in the application. The migration script will be created in the alembic/versions directory.

```
alembic revision --autogenerate -m "Initial tables"
```

The generated migration script can be applied to the database using the upgrade command.

```
(app) simha@923ed0a91d84:~/app$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> bf9e56658d31, Initial tables
(app) simha@923ed0a91d84:~/app$
```