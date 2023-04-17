import json
import colander
import deform.widget
import datetime
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

        # If no node_id is passed, form defaults are blank
        node_name_default = ""
        node_url_default = ""
        node_location_default = ""
        node_affiliation_default = ""
        node_administrator_default = ""
        node_deploy_date_default = ""
        node_support_contact_default = ""
        node_capability_data_default = ""
        node_capability_compute_default = ""

        # If node_id is passed get the node details to display in form
        if len(self.request.matchdict) > 0:
            requested_node_id = int(self.request.matchdict["node_id"])
            requested_node = DBSession.query(Node).filter_by(node_id=requested_node_id).one()
            node_name_default = requested_node.node_name
            node_url_default = requested_node.url
            node_location_default = requested_node.location
            node_affiliation_default = requested_node.affiliation
            node_administrator_default = requested_node.administrator
            node_deploy_date_default = requested_node.deploy_start_date
            node_support_contact_default = requested_node.support_contact_email
            node_capability_data_default = requested_node.data
            node_capability_compute_default = requested_node.compute

        # Used for Node Update form
        class NodeForm(colander.MappingSchema):

            node_name = colander.SchemaNode(colander.String(), default=node_name_default)
            node_url = colander.SchemaNode(colander.String(), default=node_url_default)
            location = colander.SchemaNode(colander.String(), missing="", default=node_location_default)
            affiliation = colander.SchemaNode(colander.String(), missing="", default=node_affiliation_default)
            administrator = colander.SchemaNode(
                colander.String(), missing="", default=node_administrator_default, title="Administrator"
            )
            deployed_since = colander.SchemaNode(
                colander.Date(),
                widget=deform.widget.DatePartsWidget(),
                validator=colander.Range(
                    min=datetime.date(2010, 1, 1),
                ),
                missing="",
                default=node_deploy_date_default,
                title="Deployed Since",
            )
            support_contact_email = colander.SchemaNode(
                colander.String(), missing="", default=node_support_contact_default
            )
            data = colander.SchemaNode(
                colander.Boolean(),
                widget=deform.widget.CheckboxWidget(),
                missing="",
                default=node_capability_data_default,
                label="Data",
                title="Capabilities",
            )
            compute = colander.SchemaNode(
                colander.Boolean(),
                widget=deform.widget.CheckboxWidget(),
                missing="",
                default=node_capability_compute_default,
                label="Compute",
            )

        schema = NodeForm()

        # NOTE: default method used is POST for form submit
        return deform.Form(schema, buttons=("submit",))

    @property
    def reqts(self):
        return self.node_form.get_widget_resources()

    @view_config(route_name="node_all", renderer="templates/node_update.pt")
    def display_all_nodes(self):
        form = self.node_form.render()

        # Get information from github node registry and display list of all nodes
        db = DB()
        db.add_github_node_registry()

        db_contents = DBSession.query(Node).order_by(Node.node_id)

        return dict(page_title="All Nodes", db_node=db_contents, form=form)

    @view_config(route_name="node_update", renderer="templates/node_update.pt")
    def node_update(self):
        title = "Node Update"

        # Get information from github node registry and display list of all nodes
        db = DB()
        db.add_github_node_registry()
        db_contents = DBSession.query(Node).order_by(Node.node_id)

        # Get the specific node's details to display in form
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
            location = appstruct["location"]
            affiliation = appstruct["affiliation"]
            deploystartdate = appstruct["deployed_since"]
            supportemail = appstruct["support_contact_email"]
            data = appstruct["data"]
            compute = appstruct["compute"]

            DBSession.query(Node).filter(Node.node_id == requested_node_id).update(
                {
                    Node.node_name: nodename,
                    Node.url: nodeurl,
                    Node.support_contact_email: supportemail,
                    Node.location: location,
                    Node.affiliation: affiliation,
                    Node.deploy_start_date: deploystartdate,
                    Node.data: data,
                    Node.compute: compute,
                },
                synchronize_session=False,
            )
            transaction.commit()

            # Get the newly added node information and show it in the same form
            new_added_node = DBSession.query(Node).filter_by(node_name=nodename).one()
            new_node_id = new_added_node.node_id
            url = self.request.route_url("node_update", node_id=new_node_id, page_title=title)
            return HTTPFound(url)

        return dict(page_title=title, db_node=db_contents, form=form)

    @view_config(route_name="node_info", renderer="json")
    def node_info_view(self):

        node_info_dict = {}

        requested_node_id = int(self.request.matchdict["node_id"])
        node_page = DBSession.query(Node).filter_by(node_id=requested_node_id).one()

        node_info_dict["node_name"] = node_page.node_name
        node_info_dict["node_url"] = node_page.url

        node_info_json = json.dumps(node_info_dict)

        return node_info_json
