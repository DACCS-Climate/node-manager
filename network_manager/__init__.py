from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import DBSession, Base


def main(global_config, **settings):

    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings, root_factory=".models.Root")
    config.include("cornice")
    config.include("pyramid_chameleon")

    # Add a route / path called node_home at /node for displaying all entries in the database
    config.add_route("node_home", "/node")

    # Add a route / path called node_register at /node/register.
    # This is the 'admin' page where an entry can be added to the database
    # config.add_route("node_register", "/node/register", request_method="GET")

    # Add a route / path for the particular node {node_id} at /node/info/{node_id}
    # Returns details about a particular node in json format
    # config.add_route("node_info", "/node/info/{node_id}", request_method="GET")

    # config.add_static_view("deform_static", "deform:static/")

    config.scan(".views")

    return config.make_wsgi_app()
