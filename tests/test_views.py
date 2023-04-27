from pyramid.testing import DummySecurityPolicy

# import transaction
from network_manager import models

# from pyramid.httpexceptions import HTTPNotFound

# from network_manager.models import Node


def makeUser(name, role):

    return models.User(name=name, role=role)


def setUser(config, user):

    config.set_security_policy(DummySecurityPolicy(identity=user))


def makeNode(node_id, node_name, url):

    return models.Node(node_id=node_id, node_name=node_name, url=url)


# Unit tests
class Test_nodes_info:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        nodes_info_view = node_views.nodes_info()

        return nodes_info_view

    def _addRoutes(self, config):
        config.add_route("nodes_info", "/nodes")

    def test_it(self, dummy_config, dummy_request):
        self._addRoutes(dummy_config)

        # nodes_info_response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200


class Test_node_info:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        node_info_view = node_views.node_info()

        return node_info_view

    def _addRoutes(self, config):
        config.add_route("node_info", "/node/{node_id}")

    def test_it(self, dummy_config, dummy_request):
        self._addRoutes(dummy_config)

        dummy_request.matchdict["node_id"] = 1
        # node_info_response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200


class Test_local_node_info:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        # from network_manager.db import DB

        node_views = NodeViews(request)
        # node_db = DB()

        local_node_view = node_views.local_node_info()
        # local_node_db = node_db

        return local_node_view

    def _addRoutes(self, config):
        config.add_route("local_node_info", "/node")

    def test_it(self, dummy_config, dummy_request):
        self._addRoutes(dummy_config)

        # dummy_request.matchdict["node_id"] = 1
        # local_node_info_response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200


class Test_node_edit:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        node_edit_view = node_views.node_edit()

        return node_edit_view

    def _addRoutes(self, config):
        config.add_route("node_edit", "/node/edit")

    def test_it(self, dummy_config, dummy_request):
        self._addRoutes(dummy_config)

        local_node_info_response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200
        assert "Node Update" in local_node_info_response["page_title"]
        assert "submit" in local_node_info_response["form"]


class Test_refresh_registry:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        refresh_registry_view = node_views.refresh_registry()

        return refresh_registry_view

    def _addRoutes(self, config):
        config.add_route("refresh_registry", "/refresh")

    def test_it(self, dummy_config, dummy_request):
        self._addRoutes(dummy_config)

        refresh_registry_response = self._callFUT(dummy_request)

        assert refresh_registry_response.status_code == 201
