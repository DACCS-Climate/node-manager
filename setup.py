from setuptools import setup

# export VENV=~/Documents/GitHub/node-manager/venv
# $VENV/bin/pip install -e .
# $VENV/bin/pip install -e ".[dev]"
# $VENV/bin/initialize_db development.ini
# $VENV/bin/pserve development.ini --reload



# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'deform',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_tm',
    'sqlalchemy',
    'waitress',
    'zope.sqlalchemy',
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest',
]

setup(
    name='database',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = database:main'
        ],
        'console_scripts': [

            'initialize_db = database.initialize_db:main'

        ],
    },
)