import colander
import deform.widget
import datetime

import sqlalchemy.exc
import transaction
from pyramid.httpexceptions import HTTPFound, HTTPCreated, HTTPNotFound
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

        # If node_id is passed get the node details to display in form
        requested_node = DB.local_node()
        if requested_node:
            node_name_default = requested_node.name
            node_url_default = requested_node.url
            node_location_default = requested_node.location
            node_affiliation_default = requested_node.affiliation
            node_administrator_default = requested_node.administrators
            node_deploy_date_default = requested_node.deployed_since
            node_support_contact_default = requested_node.support_contact
            node_capability_data_default = requested_node.data
            node_capability_compute_default = requested_node.compute
        else:
            node_name_default = ""
            node_url_default = ""
            node_location_default = ""
            node_affiliation_default = ""
            node_administrator_default = ""
            node_deploy_date_default = ""
            node_support_contact_default = ""
            node_capability_data_default = ""
            node_capability_compute_default = ""

        # Used for Node Update form
        class NodeForm(colander.MappingSchema):

            name = colander.SchemaNode(colander.String(), default=node_name_default)
            url = colander.SchemaNode(colander.String(), default=node_url_default)
            location = colander.SchemaNode(colander.String(), default=node_location_default)
            affiliation = colander.SchemaNode(colander.String(), default=node_affiliation_default)
            administrators = colander.SchemaNode(
                colander.String(), default=node_administrator_default, title="Administrator"
            )
            deployed_since = colander.SchemaNode(
                colander.Date(),
                widget=deform.widget.DatePartsWidget(),
                validator=colander.Range(
                    min=datetime.date(2010, 1, 1),
                ),
                default=node_deploy_date_default,
                title="Deployed Since",
            )
            support_contact = colander.SchemaNode(colander.String(), default=node_support_contact_default)
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

    @view_config(route_name="nodes_info", renderer="json")
    def nodes_info(self):
        db_contents = DBSession.query(Node).order_by(Node.id)

        return [d.as_dict() for d in db_contents]

    @view_config(route_name="node_info", renderer="json")
    def node_info(self):
        id_ = self.request.matchdict["node_id"]
        try:
            node = DBSession.query(Node).filter(Node.id == id_).one()
        except sqlalchemy.exc.NoResultFound:
            return HTTPNotFound()
        return node.as_dict()

    @view_config(route_name="local_node_info", renderer="json")
    def local_node_info(self):
        node = DB.local_node()
        if node:
            return node.as_dict()
        return {}

    @view_config(route_name="node_edit", renderer="templates/node_update.pt")
    def node_edit(self):
        if self.request.POST:
            # form has been posted
            try:
                appstruct = self.node_form.validate(self.request.POST.items())
            except deform.ValidationFailure as e:
                return dict(form=e.render())

            title = "Updated Successfully"

            with transaction.manager:
                local_node = DB.local_node()
                if DB.local_node():
                    local_node.update(appstruct, synchronize_session=False)
                else:
                    DBSession.add(Node(local=True, **appstruct))

            url = self.request.route_url("node_edit", page_title=title)
            return HTTPFound(url)
        else:
            title = "Node Update"
            form = self.node_form.render()
            return dict(page_title=title, form=form)

    @view_config(route_name="refresh_registry")
    def refresh_registry(self):
        DB.refresh_github_node_registry()
        return HTTPCreated()
