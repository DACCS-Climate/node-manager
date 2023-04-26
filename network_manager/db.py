import sqlalchemy.exc
import transaction
import datetime
from typing import Optional
from .node_registry import NodeRegistry
from .models import (
    DBSession,
    Node,
)


class DB:

    """
    Contains functions for performing database operations
    """

    @staticmethod
    def local_node() -> Optional[Node]:
        """
        Checks if the entry exists in the database using the 'local' column name in the database.

        If the entry exists it will return the entry.  Returns None otherwise.
        """
        try:
            return DBSession.query(Node).filter(Node.local).limit(1).one()
        except sqlalchemy.exc.NoResultFound:
            return None

    @staticmethod
    def refresh_github_node_registry():

        node_registry_data = NodeRegistry.get_node_registry()
        node_info_data = NodeRegistry.get_node_info()

        """
        Gets information from the github node registry repository and updates the node information if the node exists
        in the database or inserts a new record if the node does not exist in the database.
        """

        with transaction.manager:
            local_node = DB.local_node()

            nodes = []

            for name, url in node_registry_data.items():
                if local_node is None or name != local_node.name:
                    info = node_info_data[name]
                    capabilities = info.pop("capabilities")
                    try:
                        deployed_since = datetime.datetime.fromisoformat(info.pop("deployed_since"))
                    except ValueError:
                        # TODO: this is a temporary workaround until
                        #  https://github.com/DACCS-Climate/DACCS-node-registry/issues/2 is resolved
                        #  after it is resolved, this should raise an exception
                        deployed_since = datetime.datetime.now()
                    nodes.append(
                        Node(
                            **{
                                "name": name,
                                "url": url,
                                "deployed_since": deployed_since,
                                **info,
                                "data": ("data" in capabilities),
                                "compute": ("compute" in capabilities),
                            }
                        )
                    )

            DBSession.query(Node).filter(Node.local.is_(None)).delete()
            DBSession.add_all(nodes)
