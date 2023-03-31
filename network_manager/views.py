import json
import colander
import deform.widget

# from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from cornice import Service

from .models import DBSession, Node


# Used for Node Register form
class NodeForm(colander.MappingSchema):

    checkbox_choices = (
        ("weaver", "Weaver"),
        ("catalog", "Catalog"),
        ("jupyter", "Jupyter Notebook"),
    )

    node_name = colander.SchemaNode(colander.String())
    node_url = colander.SchemaNode(colander.String())
    user_email = colander.SchemaNode(colander.String())
    node_use = colander.SchemaNode(colander.Set(), widget=deform.widget.CheckboxChoiceWidget(values=checkbox_choices))

    # body = colander.SchemaNode( colander.String(), widget=deform.widget.RichTextWidget())


class NodeViews:
    # node_home = Service(name='node_home',
    #                     path='/node',
    #                     description='Get and display information about node in json.')

    node_info = Service(
        name="node_info", path="/node/info/{node_id}", description="Get and display information about node in json."
    )

    node_register = Service(name="node_register", path="/node/register", description="Add node info to database.")

    _NODEINFO = {}

    # @node_info.get()
    # def get_node_info(self, request):
    #     print("node Info keys = ")
    #     print(_NODEINFO.keys())
    #     node_info_dict = {}

    #     requested_node_id = int(self.request.matchdict["node_id"])
    #     node_page = DBSession.query(Node).filter_by(node_id=requested_node_id).one()

    # node_info_dict["node_name"] = node_page.node_name
    # node_info_dict["node_url"] = node_page.url

    #     node_info_dict["node_name"] = node_page.node_name
    #     node_info_dict["node_url"] = node_page.url

    # node_info_json = json.dumps(node_info_dict)
    #     _NODEINFO = json.dumps(node_info_dict)

    #     return _NODEINFO

    # @node_register.post()
    # def register_node_info(self):
    # form = self.node_form.render()

    # Only checks POST method data for form data
    # if "submit" in self.request.POST:

    #     controls = self.request.POST.items()

    #     try:

    #         appstruct = self.node_form.validate(controls)

    #     except deform.ValidationFailure as e:

    # Form is NOT valid

    #         return dict(form=e.render())

    # Add a new entry of node information to the database
    #     checkboxes = appstruct["node_use"]
    #     nodeuse_string = ",".join(checkboxes)

    #     nodename = appstruct["node_name"]
    #     nodeurl = appstruct["node_url"]
    #     useremail = appstruct["user_email"]
    #     nodeuse = nodeuse_string

    #     DBSession.add(Node(node_name=nodename, url=nodeurl, user_email=useremail, capabilities=nodeuse))
    # Get the newly added node information and redirect to node_info page
    #     page = DBSession.query(Node).filter_by(node_name=nodename).one()

    #     requested_node_id = page.node_id

    #     url = self.request.route_url("node_info", node_id=requested_node_id)

    #     return HTTPFound(url)

    # return dict(form=form)

    def __init__(self, request):

        self.request = request

    @property
    def node_form(self):

        schema = NodeForm()

        # NOTE: default method used is POST
        return deform.Form(schema, buttons=("submit",))

    @property
    def reqts(self):

        return self.node_form.get_widget_resources()

    # @view_config(route_name="node_home", renderer="templates/node_home.pt")
    # @node_home.get()
    @view_config(route_name="node_home", renderer="templates/node_home.pt")
    def node_home(self):

        db_contents = DBSession.query(Node).all()

        return dict(page_title="All Nodes", db_node=db_contents)

    # @view_config(route_name="node_register", renderer="templates/node_register.pt")
    @node_register.post()
    def node_register_add(self):

        form = self.node_form.render()

        # Only checks POST method data for form data
        if "submit" in self:

            controls = self.items()
            print("Controls=")
            print(controls)

            try:

                appstruct = self.node_form.validate(controls)

            except deform.ValidationFailure as e:

                # Form is NOT valid

                return dict(form=e.render())

            # Add a new entry of node information to the database
            checkboxes = appstruct["node_use"]
            nodeuse_string = ",".join(checkboxes)

            nodename = appstruct["node_name"]
            nodeurl = appstruct["node_url"]
            useremail = appstruct["user_email"]
            nodeuse = nodeuse_string

            DBSession.add(Node(node_name=nodename, url=nodeurl, user_email=useremail, capabilities=nodeuse))

            # Get the newly added node information and redirect to node_info page

            # page = DBSession.query(Node).filter_by(node_name=nodename).one()
            # requested_node_id = page.node_id
            # url = self.route_url("node_info", node_id=requested_node_id)
            # return HTTPFound(url)

        return dict(form=form)

    # @view_config(route_name="node_info", renderer="templates/node_info.pt")
    @node_info.get()
    def node_info_view(self):

        node_info_dict = {}

        requested_node_id = int(self.matchdict["node_id"])
        node_page = DBSession.query(Node).filter_by(node_id=requested_node_id).one()

        node_info_dict["node_name"] = node_page.node_name
        node_info_dict["node_url"] = node_page.url

        node_info_json = json.dumps(node_info_dict)

        return dict(node_json=node_info_json)
