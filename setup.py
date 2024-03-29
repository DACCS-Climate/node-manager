from setuptools import setup


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
    "requests",
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = ["pytest", "webtest", "pyramid_debugtoolbar"]

tests_require = [
    "pytest",
]

setup(
    name="network_manager",
    install_requires=requires,
    extras_require={
        "dev": dev_requires,
    },
    entry_points={
        "paste.app_factory": ["main = network_manager:main"],
    },
)
