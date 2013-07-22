"""The model module is repsonsible exposes the Model class, from whic user
models should derive. It also makes the 'register' function available, which
maps endpoints to their associated classes."""
from . import db, app
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from flask import current_app

def register(cls):
    """Register an endpoint with the Model class that represents it"""
    with app.app_context():
        if getattr(current_app, 'endpoint_classes', None) is None:
            current_app.endpoint_classes = {}
        if isinstance(cls, (list, tuple)):
            for entry in cls:
                current_app.endpoint_classes[entry.endpoint] = entry
        else:
            current_app.endpoint_classes[cls.endpoint] = cls
    Model.prepare(db.engine)

class DatabaseColumnDictMixin(object):
    """Set an instances database-relevant attributes from a
    dict or return a dict containing only database-column attributes of the instance."""
    def as_dict(self):
        """Return a dictionary of each of the instance's database columns and their
        associted values."""
        result_dict = {}
        for column in self.__table__.columns.keys():
            result_dict[column] = getattr(self, column, None)
        result_dict['links'] = self.links()
        return result_dict

    def from_dict(self, dictionary):
        """Set the instance's attributes based on a dictionary of instance's database columns.""" 
        for column in self.__table__.columns.keys():
            value = dictionary.get(column, None)
            if value:
                setattr(self, column, value)
        
class Resource(DatabaseColumnDictMixin):
    """A RESTful resource"""

    def resource_uri(self):
        """Return the URI at which the resource can be found.""" 
        return '/{}/{}'.format(self.endpoint, self.primary_key)

    def links(self):
        """Return a list of links for endpoints related to the resource."""
        links = []
        links.append({'rel': 'self', 'uri': self.resource_uri()})
        return links

Model = declarative_base(cls=(DeferredReflection, Resource))
