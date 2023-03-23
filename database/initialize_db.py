import os
import sys
import datetime
import transaction

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


def usage(argv):

    cmd = os.path.basename(argv[0])

    print('usage: %s <config_uri>\n'

          '(example: "%s development.ini")' % (cmd, cmd))

    sys.exit(1)


def main(argv=sys.argv):
    current_date = datetime.datetime.now()

    if len(argv) != 2:

        usage(argv)

    config_uri = argv[1]

    setup_logging(config_uri)

    settings = get_appsettings(config_uri)

    engine = engine_from_config(settings, 'sqlalchemy.')

    DBSession.configure(bind=engine)

    Base.metadata.create_all(engine)

    with transaction.manager:

         model = Node(node_id='2',
                     node_name='Node Test 2',
                     node_description='<p>Test Node</p>',
                     location='University of Toronto',
                     affiliation='DACCS',
                     url='http://www.test.com',
                     capabilities='weaver, catalog',
                     deploy_start_date= current_date,
                     user_email='test@test.com')

        # model = Page(title='Root', body='<p>Root</p>')

        DBSession.add(model)
