from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    "pyramid",
    "pyramid_chameleon",
    "waitress",
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.

# Remove pyramid_debugtoolbar before launch

dev_requires = [
    "pyramid_debugtoolbar",
    "pytest",
    "webtest",
]


# Setuptools entry point added
# Calls the 'requires' and 'dev_requires' arrays above to set the dependencies for setup()
# Install specific dependencies with the commandline and add the specifier
# $VENV/bin/pip install -e ".[dev]" -> installs only the 'dev'
setup(
    name="config",
    install_requires=requires,
    extras_require={
        "dev": dev_requires,
    },
    entry_points={
        "paste.app_factory": ["main = config:main"],
    },
)
