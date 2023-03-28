from pyramid.response import Response
from pyramid.view import view_config

# For each view return the name of that view and the
# designation that will be used for links to itself and to other views


@view_config(route_name='node_home', renderer='node_home.pt')
def node_home(request):

    return {'name': 'Node Home'}


@view_config(route_name='node_admin', renderer='node_admin.pt')
def node_admin(request):

    return {'name': 'Node Admin'}


@view_config(route_name='node_docs', renderer='node_docs.pt')
def node_docs(request):

    return {'name': 'Node Docs'}


