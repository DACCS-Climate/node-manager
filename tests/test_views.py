from pyramid.testing import DummySecurityPolicy
import transaction
from network_manager import models

# from network_manager.models import Node


def makeUser(name, role):

    return models.User(name=name, role=role)


def setUser(config, user):

    config.set_security_policy(DummySecurityPolicy(identity=user))


def makeNode(node_id, node_name, url):

    return models.Node(node_id=node_id, node_name=node_name, url=url)


# def makeNode(node_name, url):
#
#     return models.Node(node_name=node_name, url=url)


class Test_display_all_nodes:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        display_all_nodes_view = node_views.display_all_nodes()

        return display_all_nodes_view

    def _addRoutes(self, config):
        config.add_route("node_all", "/node/update")

    def test_it(self, dummy_config, dummy_request):
        # Tests that the response from the page is 200 and the page route can be found
        # Tests that the correct page title 'Node Update' is in the loaded page
        self._addRoutes(dummy_config)

        response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200
        assert response["page_title"] == "All Nodes"


class Test_node_update:
    def _callFUT(self, request):

        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        node_update_view = node_views.node_update()

        return node_update_view

    def _addRoutes(self, config):
        config.add_route("node_update", "/node/update/{node_id}")

    def test_it(self, dummy_config, dummy_request, dbsession):
        # Tests that the response from the page is 200 and the page route can be found
        # Tests that the correct page title 'Node Update' is in the loaded page
        test_node = makeNode(3, "pytestnode", "https://pytest.ca")
        with transaction.manager:
            dbsession.add(test_node)

        self._addRoutes(dummy_config)
        dummy_request.matchdict["node_id"] = 1
        node_update_test_page = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200
        assert node_update_test_page["page_title"] == "Node Update"


class Test_node_info_view:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        node_info_view = node_views.node_info_view()

        return node_info_view

    def _addRoutes(self, config):
        config.add_route("node_info", "/node/info/{node_id}")

    def test_it(self, node, dummy_config, dummy_request, dbsession):
        # Tests that the response from the page is 200 and the page route can be found
        # Tests that the returned json data contains the correct node name by comparing to a record in the database

        test_row = dbsession.query(node).filter_by(node_id=1).one()

        self._addRoutes(dummy_config)
        dummy_request.matchdict["node_id"] = 1
        node_info_response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200
        assert test_row.node_name in node_info_response
