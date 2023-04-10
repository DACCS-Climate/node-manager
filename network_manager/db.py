import os
import sys
import datetime
import transaction
from sqlalchemy import engine_from_config, insert, inspect
from .node_registry import NodeRegistry
from pyramid.paster import (
    get_appsettings,
)


from .models import (
    DBSession,
    Node,
)


class DB:
    def usage(self, argv):

        cmd = os.path.basename(argv[0])

        print("usage: %s <config_uri>\n" '(example: "%s development.ini")' % (cmd, cmd))
        print(argv)
        sys.exit(1)

    def table_exists(self, engine, name):
        inspector = inspect(engine)
        result = inspector.dialect.has_table(engine.connect(), name)

        return result

    def drop_table(self):
        argv = sys.argv
        config_uri = argv[1]
        settings = get_appsettings(config_uri)
        engine = engine_from_config(settings, "sqlalchemy.")

        # Drop test database
        Node.__table__.drop(engine)

    def check_entry(self, requested_name):

        existing_entry = DBSession.query(DBSession.query(Node).filter_by(node_name=requested_name).exists()).scalar()

        return existing_entry

    def add_new_node_entry(self, table_name, github_json):
        for key_node_name, value_url in github_json.items():
            searched_node = DBSession.query(Node).filter(Node.node_name == key_node_name)
            if searched_node is None:
                insert(table_name).values(node_name=key_node_name, url=value_url)
                transaction.commit()

    def add_github_node_registry(self):

        registry = NodeRegistry()
        github_json = registry.get_node_registry()

        current_date = datetime.datetime.now()

        # if the node name exists, update the url entry for each node name
        for key_node_name, value_url in github_json.items():

            if self.check_entry(key_node_name):

                DBSession.query(Node).filter(Node.node_name == key_node_name).update({Node.url: value_url})
                transaction.commit()

            else:
                # If the node name does not exist, add the items in the github node_registry

                with transaction.manager:

                    model = Node(
                        node_name=key_node_name,
                        node_description="",
                        location="",
                        affiliation="",
                        url=value_url,
                        capabilities="",
                        deploy_start_date=current_date,
                        user_email="",
                    )

                    DBSession.add(model)

    def initialize_db(self):

        self.add_github_node_registry()
