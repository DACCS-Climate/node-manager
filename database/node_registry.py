import os
import requests
import json


class NodeRegistry:
    def read_json(self, path):
        # project_root = "node_manager"
        # settings_path = os.path.join(project_root, 'settings.json')
        with open(path, "r") as f:
            json_content = json.load(f)

        return json_content

    def write_json(self, path, data):
        f = open(path, "w")
        json.dump(data, f, indent=4)

    def get_node_registry(self):

        curr_dir_path = os.path.dirname(os.path.realpath(__file__))
        settings_path = os.path.join(curr_dir_path, "settings", "settings.json")
        app_settings_path = os.path.join(curr_dir_path, "settings", "app_settings.json")

        app_settings = self.read_json(app_settings_path)

        node_registry_url = app_settings["node_registry_url"]
        node_registry_file = requests.get(node_registry_url, allow_redirects=True)
        node_registry_json = json.loads(node_registry_file.text)

        self.write_json(settings_path, node_registry_json)

    # Used for testing
    def main(self):

        # curr_dir_path = os.path.dirname(os.path.realpath(__file__))
        # settings_path = os.path.join(curr_dir_path, "settings", 'settings.json')
        NodeRegistry.get_node_registry(self)

        # node_registry = read_json(settings_path)

        # for entry in node_registry:
        #   print(entry)
