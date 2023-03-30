from pyramid.config import Configurator


def main(global_config, **settings):

    # Create a 'settings file' called 'home'
    # You can add settings to this through the Configurator functions
    config = Configurator(settings=settings)

    # Include Chameleon as a template renderer
    config.include("pyramid_chameleon")

    # Add a route / path called home at the root
    # Full route / path should be /home
    config.add_route("node_home", "/node")
    # homeURL = request.route_url('homeURL')

    # Add a route / path called node_docs at the /node/docs
    config.add_route("node_docs", "/node/docs")

    return config.make_wsgi_app()
