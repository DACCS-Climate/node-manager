import alembic
import alembic.config
import alembic.command
import os
from pyramid.paster import get_appsettings
from pyramid.scripting import prepare
from pyramid.testing import DummyRequest, testConfig
import pytest
import transaction

# from webob.cookies import Cookie
import webtest

from sqlalchemy import engine_from_config

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy

from network_manager import main

# from network_manager import models
from network_manager.models import Base
from network_manager.models import Node

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)


def get_engine(settings, prefix="sqlalchemy."):

    return engine_from_config(settings, prefix)


def get_session_factory(engine):

    factory = sessionmaker()

    factory.configure(bind=engine)

    return factory


def get_tm_session(session_factory, transaction_manager, request=None):
    """

    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.


    This function will hook the session to the transaction manager which

    will take care of committing any changes.


    - When using pyramid_tm it will automatically be committed or aborted

      depending on whether an exception is raised.


    - When using scripts you should wrap the session in a manager yourself.

      For example:


      .. code-block:: python


          import transaction


          engine = get_engine(settings)

          session_factory = get_session_factory(engine)

          with transaction.manager:

              dbsession = get_tm_session(session_factory, transaction.manager)


    This function may be invoked with a ``request`` kwarg, such as when invoked

    by the reified ``.dbsession`` Pyramid request attribute which is configured

    via the ``includeme`` function below. The default value, for backwards

    compatibility, is ``None``.


    The ``request`` kwarg is used to populate the ``sqlalchemy.orm.Session``'s

    "info" dict.  The "info" dict is the official namespace for developers to

    stash session-specific information.  For more information, please see the

    SQLAlchemy docs:

    https://docs.sqlalchemy.org/en/stable/orm/session_api.html#sqlalchemy.orm.session.Session.params.info


    By placing the active ``request`` in the "info" dict, developers will be

    able to access the active Pyramid request from an instance of an SQLAlchemy

    object in one of two ways:


    - Classic SQLAlchemy. This uses the ``Session``'s utility class method:


      .. code-block:: python


          from sqlalchemy.orm.session import Session as sa_Session


          dbsession = sa_Session.object_session(dbObject)

          request = dbsession.info["request"]


    - Modern SQLAlchemy. This uses the "Runtime Inspection API":


      .. code-block:: python


          from sqlalchemy import inspect as sa_inspect


          dbsession = sa_inspect(dbObject).session

          request = dbsession.info["request"]

    """

    dbsession = session_factory(info={"request": request})

    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)

    return dbsession


@pytest.fixture(scope="session")
def node():
    return Node


def pytest_addoption(parser):
    parser.addoption("--ini", action="store", metavar="INI_FILE")


@pytest.fixture(scope="session")
def ini_file(request):
    # potentially grab this path from a pytest option

    # return os.path.join(os.getcwd(), '../testing.ini')
    return os.path.abspath(request.config.option.ini or "testing.ini")
    # print('cwd')
    # print(os.getcwd())


@pytest.fixture(scope="session")
def app_settings(ini_file):
    return get_appsettings(ini_file)


@pytest.fixture(scope="session")
def dbengine(app_settings, ini_file):
    # engine = models.get_engine(app_settings)
    engine = get_engine(app_settings)

    alembic_cfg = alembic.config.Config(ini_file)
    Base.metadata.drop_all(bind=engine)
    alembic.command.stamp(alembic_cfg, None, purge=True)

    # run migrations to initialize the database
    # depending on how we want to initialize the database from scratch
    # we could alternatively call:
    # Base.metadata.create_all(bind=engine)
    # alembic.command.stamp(alembic_cfg, "head")
    alembic.command.upgrade(alembic_cfg, "head")

    yield engine

    # Base.metadata.drop_all(bind=engine)
    # alembic.command.stamp(alembic_cfg, None, purge=True)


@pytest.fixture(scope="session")
def app(app_settings, dbengine):
    return main({}, dbengine=dbengine, **app_settings)


@pytest.fixture
def tm():
    tm = transaction.TransactionManager(explicit=True)
    tm.begin()
    tm.doom()

    yield tm

    tm.abort()


@pytest.fixture
def dbsession(app, tm):

    DBSession = scoped_session(sessionmaker())
    return DBSession


@pytest.fixture
def testapp(app, tm, dbsession):
    # override request.dbsession and request.tm with our own
    # externally-controlled values that are shared across requests but aborted
    # at the end
    testapp = webtest.TestApp(
        app,
        extra_environ={
            "HTTP_HOST": "example.com",
            "tm.active": True,
            "tm.manager": tm,
            "app.dbsession": dbsession,
        },
    )

    # initialize a csrf token instead of running an initial request to get one
    # from the actual app - this only works using the CookieCSRFStoragePolicy
    testapp.set_cookie("csrf_token", "dummy_csrf_token")

    return testapp


@pytest.fixture
def app_request(app, tm, dbsession):
    """
    A real request.

    This request is almost identical to a real request but it has some
    drawbacks in tests as it's harder to mock data and is heavier.

    """
    with prepare(registry=app.registry) as env:
        request = env["request"]
        request.host = "example.com"

        # without this, request.dbsession will be joined to the same transaction
        # manager but it will be using a different sqlalchemy.orm.Session using
        # a separate database transaction
        request.dbsession = dbsession
        request.tm = tm

        yield request


@pytest.fixture
def dummy_request(tm, dbsession):
    """
    A lightweight dummy request.

    This request is ultra-lightweight and should be used only when the request
    itself is not a large focus in the call-stack.  It is much easier to mock
    and control side-effects using this object, however:

    - It does not have request extensions applied.
    - Threadlocals are not properly pushed.

    """
    request = DummyRequest()
    request.host = "example.com"
    request.dbsession = dbsession
    request.tm = tm

    return request


@pytest.fixture
def dummy_config(dummy_request):
    """
    A dummy :class:`pyramid.config.Configurator` object.  This allows for
    mock configuration, including configuration for ``dummy_request``, as well
    as pushing the appropriate threadlocals.

    """
    with testConfig(request=dummy_request) as config:
        yield config
