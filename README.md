# network-manager
Web app for Network Manager.

Lets the admin of a particular node to edit the details of their node.

Also gets information about other nodes from the node registry and stores that information locally for the admin to use.

## Requirements

Postgres database [https://www.postgresql.org/](https://www.postgresql.org/)

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

### Create the database

When installing the Postgres database it will also install pgAdmin, the graphical user interface for administrating the
database.

The installation process will guide you through setting up the database

#### Database default attributes

Create the database with the following attributes

Database name: noderegistry
Username: postgres
Password: localpassword

If you decide to use a different database name, username, and password change the postgres database connection string in the
development.ini and production.ini files to match

> POSTGRES_DATABASE_URL = postgresql+psycopg2://**username**:**password**@localhost:5432/**databasename**


### Setting the database connection

#### For postgres database (testing and production)

The database connection string will need to be set or changed in the following files:
 - development.ini
 - production.ini

##### development.ini and production.ini

Search for "sqlalchemy.url" and ensure it is set to "POSTGRES_DATABASE_URL"

> sqlalchemy.url = %(POSTGRES_DATABASE_URL)s

##### development.ini and production.ini - alembic section

Search for "Database connection strings" and ensure it is set to "POSTGRES_DATABASE_URL"

> sqlalchemy.url = %(POSTGRES_DATABASE_URL)s


### Initialize the table

#### Alembic
If the table has already been created there is no need to run anything.

If the table has not been created, run the following command in a terminal

> alembic -c development.ini upgrade head

## Start the App

### For development
> $VENV/bin/pserve development.ini --reload

### For production
> $VENV/bin/pserve production.ini --reload

## View the App

In a browser go to `http://localhost:6543/node/update`
