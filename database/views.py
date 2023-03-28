import colander
import deform.widget

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config


from .models import DBSession, Node
# Page


class NodePage(colander.MappingSchema):

    title = colander.SchemaNode(colander.String())
    # pagenodeid = colander.SchemaNode(colander.Integer())
    node_id = colander.SchemaNode(colander.Integer())
    nodename = colander.SchemaNode(colander.String())
    useremail = colander.SchemaNode(colander.String())
    nodeuse1 = colander.SchemaNode(colander.String())
    nodeuse2 = colander.SchemaNode(colander.String())
    nodeuse3 = colander.SchemaNode(colander.String())

    body = colander.SchemaNode( colander.String(), widget=deform.widget.RichTextWidget())


class NodeViews:

    def __init__(self, request):

        self.request = request

    @property
    def node_form(self):

        schema = NodePage()

        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):

        return self.node_form.get_widget_resources()

    #@view_config(route_name='home', renderer='templates/home.pt')
    #def home(self):

    #    return {'name': 'Home Page'}


    @view_config(route_name='node_home', renderer='templates/node_home.pt')
    def node_home(self):

        # db_contents = DBSession.query(Node).order_by(Node.node_id)
        db_contents = DBSession.query(Node).all()

        for node_contents in db_contents:
            node_row = vars(node_contents)
            if node_row['url'] is not None:
                print("Node ID is: " + str(node_row['node_id']) + "     URL is: " + node_row['url'])

        return dict(page_title='All Nodes',  db_node=db_contents)

    @view_config(route_name='node_register', renderer='templates/node_register.pt')
    def node_register_add(self):

        form = self.node_form.render()

        if 'submit' in self.request.params:

            controls = self.request.POST.items()

            try:

                appstruct = self.node_form.validate(controls)

            except deform.ValidationFailure as e:

                # Form is NOT valid

                return dict(form=e.render())

            # Add a new node to the database

            # new_nodeid = appstruct['node_id']
            nodename = appstruct['nodename']

            useremail = appstruct['useremail']
            nodeuse = appstruct['nodeuse1'] + "," + appstruct['nodeuse2'] + "," + appstruct['nodeuse3']
            nodeaffiliation = appstruct['nodeaffiliation']

            DBSession.add(Node(node_name=nodename,
                               user_email=useremail,
                               affiliation=nodeaffiliation,
                               capabilities=nodeuse))

            # Get the new ID and redirect

            # page = DBSession.query(Node)
            page = DBSession.query(Node).filter_by(node_name=nodename).one()

            requested_node_id = page.node_id



            url = self.request.route_url('node_info', node_id=requested_node_id)

            return HTTPFound(url)

        return dict(form=form)

    @view_config(route_name='node_info', renderer='templates/node_info.pt')
    def node_info_view(self):

        requested_node_id = int(self.request.matchdict['node_id'])
        # db_info = DBSession.query(Node).order_by(Node.node_id)

        node_page = DBSession.query(Node).filter_by(node_id=requested_node_id).one()
        # , node_id=node_page.node_id
        return dict(node_details=node_page)






