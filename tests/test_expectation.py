import pytest

# $VENV/bin/pytest tests/test_expectation.py -q


@pytest.mark.parametrize("test_input,expected", [(1, "PAVICS"), (2, "UofT")])
class NodeFunctionalTestsPyTest:

    # If the table is created, test if the information for a specific node is as expected
    # Uses sample information from the node registry
    def test_node_info_view(self, test_input, expected):
        import sys
        from sqlalchemy import engine_from_config
        from pyramid.paster import (
            get_appsettings,
            setup_logging,
        )
        from network_manager.initialize_db import table_exists

        argv = sys.argv
        config_uri = argv[1]
        setup_logging(config_uri)
        settings = get_appsettings(config_uri)

        table_name = "nodes"
        engine = engine_from_config(settings, "sqlalchemy.")

        if table_exists(engine, table_name):

            page_route = "/node/info/" + str(test_input)

            response = self.testapp.get(page_route, status=200)
            self.assertIn(expected, response.body)

    # If the table is created, test if the table contents is as expected
    def test_node_db(self, test_input, expected):
        import sys
        from sqlalchemy import engine_from_config
        from pyramid.paster import (
            get_appsettings,
            setup_logging,
        )
        from network_manager.models import DBSession, Node
        from network_manager.initialize_db import table_exists

        argv = sys.argv
        config_uri = argv[1]
        setup_logging(config_uri)
        settings = get_appsettings(config_uri)

        table_name = "nodes"
        engine = engine_from_config(settings, "sqlalchemy.")

        if table_exists(engine, table_name):
            db_entry = DBSession.query(Node).filter_by(node_id=test_input).one()
            assert db_entry.node_name == expected
