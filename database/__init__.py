from pyramid.config import Configurator


from sqlalchemy import engine_from_config


from .models import DBSession, Base, Node


def main(global_config, **settings):

    engine = engine_from_config(settings, "sqlalchemy.")

    DBSession.configure(bind=engine)

    Base.metadata.bind = engine

    config = Configurator(settings=settings, root_factory=".models.Root")

    config.include("pyramid_chameleon")

    # Add a route / path called node_home at /node
    # config.add_route("home", "/")

    # Add a route / path called node_home at /node
    config.add_route("node_home", "/node")

    # Add a route / path called node_admin at /node/admin
    config.add_route("node_admin", "/node/admin")

    # Add a route / path called node_register at /node/register
    config.add_route("node_register", "/node/register")

    # Add a route / path for the particular node {node_id} at /node/info/{node_id}
    config.add_route("node_info", "/node/info/{node_id}")

    config.add_static_view("deform_static", "deform:static/")

    config.scan(".views")

    return config.make_wsgi_app()
