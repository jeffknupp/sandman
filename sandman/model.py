"""The model module is repsonsible exposes the :class:`sandman.Resource` class, from which user
models should derive. It also makes the :func:`register` function available, which
maps endpoints to their associated classes."""

from decimal import Decimal
from . import db, app
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from flask import current_app

__all__ = ['Model', 'register']

def register(cls):
    """Register with the API a :class:`sandman.Resource` class and associated
    endpoint.
    
    :param cls: User-defined class derived from :class:`sandman.Resource` to be
                registered with the endpoint returned by :func:`endpoint()`
    :type cls: :class:`sandman.Resource` or tuple
    
    """
    with app.app_context():
        if getattr(current_app, 'endpoint_classes', None) is None:
            current_app.endpoint_classes = {}
        if isinstance(cls, (list, tuple)):
            for entry in cls:
                current_app.endpoint_classes[entry.endpoint()] = entry
        else:
            current_app.endpoint_classes[cls.endpoint()] = cls
    Model.prepare(db.engine)

       
class Resource(object):
    """A mixin class containing the majority of the RESTful API functionality.
    
    :class:`sandman.Resource` is the base class of `:class:`sandman.Model`,
    from which user models are derived.
    """

    # override :attr:`__endpoint__` if you wish to configure the
    # :class:`sandman.Resource`'s endpoint. 
    #
    # Default: __tablename__ in lowercase and pluralized
    __endpoint__ = None

    # override :attr:`__methods__` if you wish to change the HTTP methods 
    # this :class:`sandman.Resource` supports.
    #
    # Default: ``('GET', 'POST', 'PATCH', 'DELETE', 'PUT')``
    __methods__ = ('GET', 'POST', 'PATCH', 'DELETE', 'PUT')

    @classmethod
    def endpoint(cls):
        """Return the :class:`sandman.Resource`'s endpoint.

        :rtype: string

        """
        if cls.__endpoint__ is not None:
            return cls.__endpoint__
        return cls.__tablename__.lower() + 's'

    def resource_uri(self):
        """Return the URI at which the resource can be found.
        
        :rtype: string

        """ 
        primary_key_value = getattr(self, self.primary_key(), None)
        return '/{}/{}'.format(self.endpoint(), primary_key_value)

    def links(self):
        """Return a list of links for endpoints related to the resource."""
        links = []
        links.append({'rel': 'self', 'uri': self.resource_uri()})
        return links

    @classmethod
    def primary_key(cls):
        """Return the name of the table's primary key
        
        :rtype: string

        """

        return cls.__table__.primary_key.columns.values()[0].name

    def as_dict(self):
        """Return a dictionary containing only the attributes which map to 
        an instance's database columns.
        
        :rtype: dict

        """ 
        result_dict = {}
        for column in self.__table__.columns.keys():
            result_dict[column] = getattr(self, column, None)
            if isinstance(result_dict[column], Decimal):
                result_dict[column] = str(result_dict[column])
        result_dict['links'] = self.links()
        return result_dict

    def from_dict(self, dictionary):
        """Set a set of attributes which correspond to the 
        :class:`sandman.Resource`'s columns.

        :param dict dictionary: A dictionary of attributes to set on the
        instance whose keys are the column names of the :class:`sandman.Resource`'s
        underlying database table. 
        
        """ 
        for column in self.__table__.columns.keys():
            value = dictionary.get(column, None)
            if value:
                setattr(self, column, value)

    def replace(self, dictionary):
        """Set all attributes which correspond to the 
        :class:`sandman.Resource`'s columns to the values in *dictionary*,
        inserting None if an attribute's value is not specified.

        :param dict dictionary: A dictionary of attributes to set on the
        instance whose keys are the column names of the :class:`sandman.Resource`'s
        underlying database table. 

        """
        for column in self.__table__.columns.keys():
                setattr(self, column, None)
        self.from_dict(dictionary)
 
Model = declarative_base(cls=(DeferredReflection, Resource))
