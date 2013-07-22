from . import db
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
Base = declarative_base(cls=DeferredReflection)

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
        return '/{}/{}'.format(self.endpoint, self.primary_key())

    def links(self):
        """Get a list of links for possible actions on this resource"""
        links = []
        links.append({'rel': 'self', 'uri': self.resource_uri()})
        return links

print (db.engine.table_names())
Base.prepare(db.engine)
