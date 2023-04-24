import requests
from .constants import NM_NODE_REGISTRY_URL, NM_NODE_INFO_URL


class NodeRegistry:
    """
    Contains functions for retrieving information from the github node registry
    """

    # Gets node_registry.json from github and returns the content
    def get_node_registry(self):
        """
        Gets information from the node registry repository at the given url.
        Returns the information in json format
        """

        node_registry_url = NM_NODE_REGISTRY_URL
        node_registry_file = requests.get(node_registry_url, allow_redirects=True)
        node_registry_json = node_registry_file.json()

        return node_registry_json

    def get_node_info(self):
        """
        Gets information from the node info repository at the given url.
        Returns the information in json format
        """

        node_info_url = NM_NODE_INFO_URL
        node_info_file = requests.get(node_info_url, allow_redirects=True)
        node_info_json = node_info_file.json()

        return node_info_json
