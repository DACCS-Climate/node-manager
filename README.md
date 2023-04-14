# network-manager
Web app for Network Manager.

Lets the admin of a particular node to edit the details of their node.

Also gets information about other nodes from the node registry and stores that information locally for the admin to use.

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

### For postgres database (testing and production)

The database connection string will need to be set or changed in the following files:
 - development.ini
 - production.ini

#### development.ini and production.ini

Search for "sqlalchemy.url" and ensure it is set to "POSTGRES_DATABASE_URL"

> sqlalchemy.url = %(POSTGRES_DATABASE_URL)s

#### development.ini and production.ini - alembic section

Search for "Database connection strings" and ensure it is set to "POSTGRES_DATABASE_URL"

> sqlalchemy.url = %(POSTGRES_DATABASE_URL)s


## Initialize the table


### Alembic
If the database and table has already been created there is no need to run anything.

If the database and table has not been created, install Postgres, set up the database, and run the following command in a terminal

> alembic upgrade head


## Start the App

### For development
> $VENV/bin/pserve development.ini --reload

### For production
> $VENV/bin/pserve production.ini --reload

## View the App

In a browser go to `http://localhost:6543/node/update`
