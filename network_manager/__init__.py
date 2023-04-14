from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import DBSession, Base


def main(global_config, **settings):

    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include("pyramid_chameleon")

    # Add a route / path called node_all at /node/update
    # This is the 'admin' page
    # This is for displaying all entries in the database at the top of the page and a blank form
    config.add_route("node_all", "/node/update")

    # "Get and display information about node in json."
    config.add_route("node_info", "/node/info/{node_id}")

    # Add a route / path called node_update at /node/update.
    # This is the 'admin' page where a specific node's details can be updated in the database
    config.add_route("node_update", "/node/update/{node_id}")

    config.add_static_view("deform_static", "deform:static/")

    config.scan(".views")

    return config.make_wsgi_app()
