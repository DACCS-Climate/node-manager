import datetime
import transaction
from sqlalchemy import insert
from .node_registry import NodeRegistry
from .models import (
    DBSession,
    Node,
)


class DB:
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
        node_registry_json = registry.get_node_registry()
        # node_info_json = registry.get_node_info()

        current_date = datetime.datetime.now()

        # if the node name exists, update the url entry for each node name
        for key_node_name, value_url in node_registry_json.items():

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
                        support_contact_email="",
                        deploy_start_date=current_date,
                        data=None,
                        compute=None,
                        administrator="",
                    )

                    DBSession.add(model)
