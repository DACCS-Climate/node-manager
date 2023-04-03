from pyramid.config import Configurator


def main(global_config, **settings):
    # Create a 'settings file' called 'config'
    # You can add settings to this through the Configurator functions
    config = Configurator(settings=settings)

    # Include Chameleon as a template renderer
    config.include("pyramid_chameleon")

    # Add a route / path called home at the root
    # Full route / path should be /home
    config.add_route("home", "/")
    # homeURL = request.route_url('homeURL')

    # Add a route / path called docs at /docs
    config.add_route("docs", "/docs")

    # Add a route / path called jupyter at /docs/jupyter
    config.add_route("jupyter", "/docs/jupyter")

    # Add a route / path called weaver at the /weaver
    config.add_route("weaver", "/weaver")

    # Add a route / path called catalog at /catalog
    config.add_route("catalog", "/catalog")

    # Add a route / path called login at /login
    config.add_route("login", "/login")

    # Add a route / path called admin at /admin
    config.add_route("admin", "/admin")

    # Check the 'views' file for any views that have been set
    config.scan(".views")

    return config.make_wsgi_app()
