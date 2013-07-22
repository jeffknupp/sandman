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
        current_app.endpoint_classes[cls.endpoint] = cls
    Model.prepare(db.engine)

class DictMixin(object):
    def as_dict(self):
        result_dict = {}
        for column in self.__table__.columns.keys():
            result_dict[column] = getattr(self, column, None)
        result_dict['links'] = self.links()
        return result_dict

    def from_dict(self, dictionary):
        for column in self.__table__.columns.keys():
            value = dictionary.get(column, None)
            setattr(self, column, value)
        
class Resource(DictMixin):
    def resource_uri(self):
        return '/{}/{}'.format(self.endpoint, self.primary_key)

    def links(self):
        """Get a list of links for possible actions on this resource"""
        links = []
        links.append({'rel': 'self', 'uri': self.resource_uri()})
        return links

Model = declarative_base(cls=(DeferredReflection, Resource))
