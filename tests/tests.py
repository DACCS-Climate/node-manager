import unittest
import transaction
from pyramid import testing


# $VENV/bin/pytest tests/tests.py -q


def _initTestingDB():

    from sqlalchemy import create_engine

    from network_manager.models import (
        DBSession,
        Base,
        Node,
    )

    engine = create_engine("sqlite://")

    Base.metadata.create_all(engine)

    DBSession.configure(bind=engine)

    with transaction.manager:

        model = Node(node_name="node test", node_description="This is the description for node test")

        DBSession.add(model)

    return DBSession


class NodeViewTests(unittest.TestCase):
    def setUp(self):

        self.session = _initTestingDB()

        self.config = testing.setUp()

    def tearDown(self):

        self.session.remove()

        testing.tearDown()

    def test_node_home_view(self):
        from network_manager.views import NodeViews

        request = testing.DummyRequest()
        inst = NodeViews(request)
        response = inst.node_home()

        self.assertEqual(response["page_title"], "All Nodes")

    def test_node_register_view(self):
        from network_manager.views import NodeViews

        request = testing.DummyRequest()
        inst = NodeViews(request)
        response = inst.node_register()

        self.assertEqual(response["page_title"], "Node Register")


class NodeFunctionalTests(unittest.TestCase):
    def setUp(self):

        from pyramid.paster import get_app

        app = get_app("development.ini")

        from webtest import TestApp

        self.testapp = TestApp(app)

    def tearDown(self):

        from network_manager.models import DBSession

        DBSession.remove()
