from pyramid.authorization import Allow, Everyone
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import register

from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Text,
    DateTime,
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

DBSession = scoped_session(sessionmaker())
register(DBSession)

Base = declarative_base()


# Define model for node table
class Node(Base):

    __tablename__ = "nodes"

    node_id = Column(Integer, primary_key=True, autoincrement=True)

    node_name = Column(Text, unique=True)
    node_description = Column(Text)
    location = Column(Text)
    affiliation = Column(Text)
    url = Column(Text, unique=True)
    support_contact_email = Column(Text)
    deploy_start_date = Column(DateTime)
    data = Column(Boolean, default=False)
    compute = Column(Boolean, default=False)
    administrator = Column(Text)


# Root Factory
# Used for building access control list
class Root:
    __acl__ = [(Allow, Everyone, "view"), (Allow, "group:editors", "edit")]

    def __init__(self, request):
        self.request = request
