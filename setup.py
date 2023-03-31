from setuptools import setup

# export VENV=~/Documents/GitHub/node-manager/venv
# $VENV/bin/pip install -e .
# $VENV/bin/pip install -e ".[dev]"
# $VENV/bin/initialize_db development.ini
# $VENV/bin/pserve development.ini --reload


# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    "deform",
    "postgres",
    "psycopg2-binary",
    "alembic",
    "pyramid",
    "pyramid_chameleon",
    "pyramid_tm",
    "cornice",
    "sqlalchemy",
    "waitress",
    "zope.sqlalchemy",
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = [
    "pyramid_debugtoolbar",
    "pytest",
    "webtest",
]

setup(
    name="network_manager",
    install_requires=requires,
    extras_require={
        "dev": dev_requires,
    },
    entry_points={
        "paste.app_factory": ["main = network_manager:main"],
        "console_scripts": ["initialize_db = network_manager.initialize_db:main"],
    },
)
