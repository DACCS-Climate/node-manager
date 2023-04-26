from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import DBSession, Base


def main(global_config, **settings):

    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)

    config.include("pyramid_chameleon")

    config.add_route("node_edit", "/node/edit", request_method=("POST", "GET"))

    config.add_route("node_info", "/node/{node_id}", request_method="GET")

    config.add_route("local_node_info", "/node", request_method="GET")

    config.add_route("nodes_info", "/nodes", request_method="GET")

    config.add_route("refresh_registry", "/refresh", request_method="PATCH")

    config.add_static_view("deform_static", "deform:static/")

    config.scan(".views")

    return config.make_wsgi_app()
