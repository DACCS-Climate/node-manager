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
    """
    Defines the "nodes" table for use in sqlalchemy
    """

    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    location = Column(Text, nullable=False)
    affiliation = Column(Text, nullable=False)
    url = Column(Text, unique=True, nullable=False)
    support_contact = Column(Text, nullable=False)
    deployed_since = Column(DateTime, nullable=False)
    data = Column(Boolean, default=False, nullable=False)
    compute = Column(Boolean, default=False, nullable=False)
    administrators = Column(Text)
    local = Column(Boolean, nullable=True, default=None)

    def as_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d["deployed_since"] = d["deployed_since"].isoformat()
        return d
