import json
import colander
import deform.widget
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .models import DBSession, Node
from .db import DB


class NodeViews:
    def __init__(self, request):

        self.request = request

    @property
    def node_form(self):
        # On page load get the passed node ID and get the node details to populate the form fields
        requested_node_id = int(self.request.matchdict["node_id"])
        requested_node = DBSession.query(Node).filter_by(node_id=requested_node_id).one()

        # Used for Node Register form
        class NodeForm(colander.MappingSchema):

            node_name = colander.SchemaNode(colander.String(), default=requested_node.node_name)
            node_url = colander.SchemaNode(colander.String(), default=requested_node.url)
            user_email = colander.SchemaNode(colander.String(), default=requested_node.user_email)
            weaver = colander.SchemaNode(
                colander.Boolean(),
                widget=deform.widget.CheckboxWidget(),
                default=requested_node.weaver,
                label="Weaver",
                title="Capabilities",
            )
            catalog = colander.SchemaNode(
                colander.Boolean(),
                widget=deform.widget.CheckboxWidget(),
                default=requested_node.catalog,
                label="Catalog",
            )
            jupyter = colander.SchemaNode(
                colander.Boolean(),
                widget=deform.widget.CheckboxWidget(),
                default=requested_node.jupyter,
                label="Jupyter",
            )

        schema = NodeForm()

        # NOTE: default method used is POST for form submit
        return deform.Form(schema, buttons=("submit",))

    @property
    def reqts(self):

        return self.node_form.get_widget_resources()

    @view_config(route_name="node_home", renderer="templates/node_home.pt")
    def node_home(self):

        db = DB()
        db.add_github_node_registry()

        db_contents = DBSession.query(Node).order_by(Node.node_id)

        return dict(page_title="All Nodes", db_node=db_contents)

    @view_config(route_name="node_update", renderer="templates/node_update.pt")
    def node_update(self):
        title = "Node Update"

        requested_node_id = int(self.request.matchdict["node_id"])

        form = self.node_form.render()

        # Checks for the submit button, then uses POST to get the submitted information
        # If not, display form using GET
        if "submit" in self.request.params:

            controls = self.request.POST.items()

            try:

                appstruct = self.node_form.validate(controls)

            except deform.ValidationFailure as e:

                # Form is NOT valid

                return dict(form=e.render())

            title = "Updated Successfully"
            # Updates entry of node information to the database
            nodename = appstruct["node_name"]
            nodeurl = appstruct["node_url"]
            useremail = appstruct["user_email"]
            weaver = appstruct["weaver"]
            catalog = appstruct["catalog"]
            jupyter = appstruct["jupyter"]

            DBSession.query(Node).filter(Node.node_id == requested_node_id).update(
                {
                    Node.node_name: nodename,
                    Node.url: nodeurl,
                    Node.user_email: useremail,
                    Node.weaver: weaver,
                    Node.catalog: catalog,
                    Node.jupyter: jupyter,
                },
                synchronize_session=False,
            )
            transaction.commit()

            # Get the newly added node information and redirect to Node Added Successfully page
            new_added_node = DBSession.query(Node).filter_by(node_name=nodename).one()
            new_node_id = new_added_node.node_id
            url = self.request.route_url("node_added", new_node_id=new_node_id, page_title=title)
            return HTTPFound(url)

        return dict(page_title=title, form=form)

    @view_config(route_name="node_added", renderer="templates/node_added_view.pt")
    def node_added_view(self):

        new_node_id = int(self.request.matchdict["new_node_id"])

        new_node_entry = DBSession.query(Node).filter_by(node_id=new_node_id).one()

        return dict(page_title="Node Register", new_node=new_node_entry)

    @view_config(route_name="node_info", renderer="json")
    def node_info_view(self):

        node_info_dict = {}

        requested_node_id = int(self.request.matchdict["node_id"])
        node_page = DBSession.query(Node).filter_by(node_id=requested_node_id).one()

        node_info_dict["node_name"] = node_page.node_name
        node_info_dict["node_url"] = node_page.url

        node_info_json = json.dumps(node_info_dict)

        return dict(node_json=node_info_json)
