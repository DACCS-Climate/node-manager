from pyramid.response import Response
from pyramid.view import view_config


# For each view return the name of that view and the designation that will be used for links to itself and to other views
@view_config(route_name="home", renderer="home.pt")
def home(request):
    return {
        "name": "Home View",
        "home": "Home",
        "docs": "Documentation",
        "jupyter": "Jupyter",
        "weaver": "Weaver",
        "catalog": "Catalog",
        "login": "Login",
        "admin": "Admin",
    }


@view_config(route_name="docs", renderer="home.pt")
def docs(request):
    return {
        "name": "Documentation View",
        "home": "Home",
        "docs": "Documentation",
        "jupyter": "Jupyter",
        "weaver": "Weaver",
        "catalog": "Catalog",
        "login": "Login",
        "admin": "Admin",
    }


@view_config(route_name="jupyter", renderer="home.pt")
def jupyter(request):
    return {
        "name": "Jupyter View",
        "home": "Home",
        "docs": "Documentation",
        "jupyter": "Jupyter",
        "weaver": "Weaver",
        "catalog": "Catalog",
        "login": "Login",
        "admin": "Admin",
    }


@view_config(route_name="weaver", renderer="home.pt")
def weaver(request):
    return {
        "name": "Weaver View",
        "home": "Home",
        "docs": "Documentation",
        "jupyter": "Jupyter",
        "weaver": "Weaver",
        "catalog": "Catalog",
        "login": "Login",
        "admin": "Admin",
    }


@view_config(route_name="catalog", renderer="home.pt")
def catalog(request):
    return {
        "name": "Catalog View",
        "home": "Home",
        "docs": "Documentation",
        "jupyter": "Jupyter",
        "weaver": "Weaver",
        "catalog": "Catalog",
        "login": "Login",
        "admin": "Admin",
    }


@view_config(route_name="login", renderer="home.pt")
def login(request):
    return {
        "name": "Login View",
        "home": "Home",
        "docs": "Documentation",
        "jupyter": "Jupyter",
        "weaver": "Weaver",
        "catalog": "Catalog",
        "login": "Login",
        "admin": "Admin",
    }


@view_config(route_name="admin", renderer="home.pt")
def admin(request):
    return {
        "name": "Admin View",
        "home": "Home",
        "docs": "Documentation",
        "jupyter": "Jupyter",
        "weaver": "Weaver",
        "catalog": "Catalog",
        "login": "Login",
        "admin": "Admin",
    }
