# node-manager
Web app for node manager

# Requirements

FastAPI - [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

# Development

## Style Checking

Coding style is enforced using the [pre-commit](https://pre-commit.com/) package.

You can set up your local git repository so that these style checks are automatically triggered whenever you
make a new commit.

```shell
pip install pre-commit  # Install the pre-commit package
pre-commit install      # Install the pre-commit hooks defined in .pre-commit-config.yaml to the .git/ directory for this repo
```

Now whenever you make a commit, the style checks will run automatically and suggest changes to your code!
=======
# Running the App

Some things need to be done first before starting the app.


## Set Virtual Environment

If needed, set the environment variable.  Change the path as needed, but keep the last folder as 'venv'

> export VENV=~/Documents/GitHub/node-manager/venv

## Install Dependencies

Run after setting environment variable

> $VENV/bin/pip install -e .
>
> $VENV/bin/pip install -e ".[dev]"

## Initialize the Database

### For sqlite database (testing only)

The database connection string will need to be set or changed in the following files:
 - development.ini
 - alembic.ini

#### development.ini

Search for "sqlalchemy.url" and ensure it is set to "SQLITE_DATABASE_URL"

> sqlalchemy.url = %(SQLITE_DATABASE_URL)s

#### alembic.ini

Search for "Database connection strings" and ensure the one for sqlite is uncommented

> sqlalchemy.url = sqlite:///%(here)s/sqltutorial.sqlite


### For postgres database (testing and production)

The database connection string will need to be set or changed in the following files:
 - development.ini
 - alembic.ini

#### development.ini

Search for "sqlalchemy.url" and ensure it is set to "POSTGRES_DATABASE_URL"

> sqlalchemy.url = %(POSTGRES_DATABASE_URL)s

#### alembic.ini

Search for "Database connection strings" and ensure the one for postgres is uncommented

> sqlalchemy.url = postgresql+psycopg2://postgres:localpassword@localhost:5432/noderegistry


## Initialize the table

### For sqlite database

> $VENV/bin/initialize_db development.ini

### For postgres database

#### Alembic
If the database and table has already been created there is no need to run anything.

If the database and table has not been created, install Postgres, set up the database, and run the following command in a terminal

> alembic upgrade head


## Start the App

### For development
> $VENV/bin/pserve development.ini --reload

### For production
> $VENV/bin/pserve production.ini --reload

## View the App

In a browser go to `http://localhost:6543/node`
