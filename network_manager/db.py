import datetime
import transaction
from sqlalchemy import insert
from .node_registry import NodeRegistry
from .models import (
    DBSession,
    Node,
)


class DB:
    """
    Contains functions for performing database operations
    """

    def check_entry(self, requested_name):
        """
        Checks if the entry exists in the database using the passed node name.

        If the entry exists it will return True.  Returns False otherwise.
        """

        existing_entry = DBSession.query(DBSession.query(Node).filter_by(node_name=requested_name).exists()).scalar()

        return existing_entry

    def add_new_node_entry(self, table_name, github_json):
        """
        Adds a new entry into the database.

        Takes the table name and the node information retrieved from the github repository.
        If the node name is not found a new record is inserted into the database with that specific node name and url.
        """
        for key_node_name, value_url in github_json.items():
            searched_node = DBSession.query(Node).filter(Node.node_name == key_node_name)
            if searched_node is None:
                insert(table_name).values(node_name=key_node_name, url=value_url)
                transaction.commit()

    def add_github_node_registry(self):
        """
        Gets information from the github node registry repository and updates the node information if the node exists
        in the database or inserts a new record if the node does not exist in the database.
        """
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
