# import pytest
# import requests
# import requests_mock

from pyramid.testing import DummySecurityPolicy
import datetime

from network_manager import models


def makeUser(name, role):

    return models.User(name=name, role=role)


def setUser(config, user):

    config.set_security_policy(DummySecurityPolicy(identity=user))


def makeNode(node_id, node_name, url, location, affiliation, support_contact, deployed_since, data, compute, local):

    return models.Node(
        id=node_id,
        name=node_name,
        url=url,
        location=location,
        affiliation=affiliation,
        support_contact=support_contact,
        deployed_since=deployed_since,
        data=data,
        compute=compute,
        local=local,
    )


# Unit tests
class Test_nodes_info:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        nodes_info_view = node_views.nodes_info()

        return nodes_info_view

    def _addRoutes(self, config):
        config.add_route("nodes_info", "/nodes")

    def test_it(self, dummy_config, dummy_request, dbsession, tm):
        deployed_since = datetime.datetime.now()

        testNode = makeNode(
            1,
            "test_node1",
            "www.testurl1.com",
            "test location1",
            "test affiliation1",
            "test contact",
            deployed_since,
            True,
            True,
            False,
        )

        try:
            dbsession.add(testNode)
            dbsession.commit()
        except Exception:
            dbsession.rollback()
            raise
        finally:
            dbsession.close()

        self._addRoutes(dummy_config)
        dummy_request.context = testNode
        nodes_info_response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200
        assert nodes_info_response[0]["name"] == "test_node1"


class Test_node_info:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        node_info_view = node_views.node_info()

        return node_info_view

    def _addRoutes(self, config):
        config.add_route("node_info", "/node/{node_id}")

    def test_it(self, dummy_config, dummy_request, dbsession, tm):
        deployed_since = datetime.datetime.now()

        testNode = makeNode(
            2,
            "test_node2",
            "www.testurl2.com",
            "test location2",
            "test affiliation2",
            "test contact",
            deployed_since,
            True,
            True,
            False,
        )
        try:
            dbsession.add(testNode)
            dbsession.commit()
        except Exception:
            dbsession.rollback()
            raise
        finally:
            dbsession.close()

        self._addRoutes(dummy_config)

        dummy_request.matchdict["node_id"] = 2
        node_info_response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200
        assert node_info_response["name"] == "test_node2"


class Test_local_node_info:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)

        local_node_view = node_views.local_node_info()

        return local_node_view

    def _addRoutes(self, config):
        config.add_route("local_node_info", "/node")

    def test_it(self, dummy_config, dummy_request, dbsession, tm):
        self._addRoutes(dummy_config)

        deployed_since = datetime.datetime.now()

        testNode = makeNode(
            3,
            "test_local_node_info",
            "www.testurl3.com",
            "test location",
            "test affiliation",
            "test contact",
            deployed_since,
            True,
            True,
            True,
        )

        try:
            dbsession.add(testNode)
            dbsession.commit()
        except Exception:
            dbsession.rollback()
            raise
        finally:
            dbsession.close()

        local_node_info_response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200
        assert local_node_info_response["name"] == "test_local_node_info"
        assert local_node_info_response["name"] != "test_node1"


class Test_node_edit_GET:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        node_edit_view = node_views.node_edit()

        return node_edit_view

    def _addRoutes(self, config):
        config.add_route("node_edit", "/node/edit")

    def test_it(self, dummy_config, dummy_request):
        self._addRoutes(dummy_config)
        # test_request_get = requests_mock.get('http://localhost:6543/node/edit', text='mockertest')

        dummy_request.GET = {}

        local_node_info_response = self._callFUT(dummy_request)

        assert dummy_request.response.status_code == 200
        assert "Node Update" in local_node_info_response["page_title"]
        assert "submit" in local_node_info_response["form"]


# @requests_mock.Mocker()
class Test_node_edit_POST:
    def _callFUT(self, request):
        from network_manager.views import NodeViews

        node_views = NodeViews(request)
        node_edit_view = node_views.node_edit()

        return node_edit_view

    def _addRoutes(self, config):
        config.add_route("node_edit", "/node/edit")

    # @requests_mock.Mocker()
    def test_it(self, dummy_config, dummy_request, requests_mock):

        self._addRoutes(dummy_config)

        # requests_mock_post = requests_mock.post('http://localhost:6543/node/edit', text='mockposttest')

        request_POST_items = {
            "name": "node_edit_post_info",
            "url": "www.testurl3.com",
            "location": "test location",
            "affiliation": "test affiliation",
            "administrators": "test admin",
            "deployed_since": {"year": "2023", "month": "5", "day": "1"},
            "support_contact": "test contact",
            "data": "True",
            "compute": "True",
            "local": True,
        }

        dummy_request.POST = request_POST_items

        local_node_info_response = self._callFUT(dummy_request)

        assert "Node Update" in local_node_info_response["page_title"]
        assert "submit" in local_node_info_response["form"]
        assert local_node_info_response["name"] == "node_edit_post_info"
        assert dummy_request.response.status_code == 200

        # assert 'mockposttest' == requests_mock_post.text


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
