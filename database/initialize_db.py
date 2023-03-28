import os
import sys
import datetime
import transaction
import requests

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )


from .models import (

    DBSession,
    Node,
    Base,
    # Page,

    )


from database.node_registry import NodeRegistry



# $VENV/bin/initialize_db development.ini
def usage(argv):

    cmd = os.path.basename(argv[0])

    print('usage: %s <config_uri>\n'

          '(example: "%s development.ini")' % (cmd, cmd))

    sys.exit(1)





def main(argv=sys.argv):
    curr_dir_path = os.path.dirname(os.path.realpath(__file__))
    settings_path = os.path.join(curr_dir_path, "settings", 'settings.json')

    registry = NodeRegistry()
    registry.get_node_registry()

    github_json = registry.read_json(settings_path)


    current_date = datetime.datetime.now()


    if len(argv) != 2:

        usage(argv)

    config_uri = argv[1]
    setup_logging(config_uri)

    settings = get_appsettings(config_uri)

    engine = engine_from_config(settings, 'sqlalchemy.')

    DBSession.configure(bind=engine)

    Base.metadata.create_all(engine)

    Node.nodes.drop(engine)

    for key_node_name, value_url in github_json.items():


        with transaction.manager:
            # node_id='2',
            model = Node(
                         node_name=key_node_name,
                         node_description='',
                         location='',
                         affiliation='',
                         url=value_url,
                         capabilities='',
                         deploy_start_date= current_date,
                         user_email='')

            DBSession.add(model)


