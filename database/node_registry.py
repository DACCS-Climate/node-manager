import os
import requests
import json


class NodeRegistry:

    def read_json(self, path):
        # project_root = "node_manager"
        # settings_path = os.path.join(project_root, 'settings.json')
        with open(path, 'r') as f:
            json_content = json.load(f)



        return json_content


    def write_json(self, path, data):
        f = open(path, 'w')
        json.dump(data, f, indent=4)


    def get_node_registry(self):
        settings_dict={}
        curr_dir_path = os.path.dirname(os.path.realpath(__file__))
        settings_path = os.path.join(curr_dir_path, "settings", 'settings.json')

        github_url = "https://raw.githubusercontent.com/DACCS-Climate/DACCS-node-registry/main/node_registry.json"
        node_registry_file = requests.get(github_url, allow_redirects=True)
        node_registry_json = json.loads(node_registry_file.text)

        # for key, value in node_registry_json.items():
         #    if not settings_dict:
         #        settings_dict["node_name"] = key
         #        settings_dict["node_url"] = value
         #    else:
         #        settings_dict['node_name'].append(key)
         #        settings_dict['node_url'].append(value)
            # print("Key=" + key + "   Value=" + value)

        self.write_json(settings_path, node_registry_json)
        # print(curr_dir_path)
        # f = open(settings_path, 'w')
        # json.dump(node_registry_json,f, indent=4)



    def main(self):
        # curr_dir_path = os.path.dirname(os.path.realpath(__file__))
        # settings_path = os.path.join(curr_dir_path, "settings", 'settings.json')
        NodeRegistry.get_node_registry(self)

        # node_registry = read_json(settings_path)

        #for entry in node_registry:
         #   print(entry)


curr_dir_path = os.path.dirname(os.path.realpath(__file__))
settings_path = os.path.join(curr_dir_path, "settings", 'settings.json')

# print(curr_dir_path)
x = NodeRegistry()
# x.main()
# github_json = x.read_json(settings_path)



# print(github_json)