import requests
import json
from .constants import NM_NODE_REGISTRY_URL, NM_NODE_INFO_URL


class NodeRegistry:

    # Gets node_registry.json from github and returns the content
    def get_node_registry(self):

        node_registry_url = NM_NODE_REGISTRY_URL
        node_registry_file = requests.get(node_registry_url, allow_redirects=True)
        node_registry_json = json.loads(node_registry_file.text)

        return node_registry_json

    def get_node_info(self):

        node_info_url = NM_NODE_INFO_URL
        node_info_file = requests.get(node_info_url, allow_redirects=True)
        node_info_json = json.loads(node_info_file.text)

        return node_info_json
