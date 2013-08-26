"""The Model class is meant to be the base class for user Models. It represents
a table in the database that should be modeled as a resource."""

from decimal import Decimal
from sandman import app
from flask import current_app

class Model(object):
    """A mixin class containing the majority of the RESTful API functionality.

    :class:`sandman.model.Model` is the base class of `:class:`sandman.Model`,
    from which user models are derived.
    """

    __endpoint__ = None
    """override :attr:`__endpoint__` if you wish to configure the
    :class:`sandman.model.Model`'s endpoint.

    Default: __tablename__ in lowercase and pluralized
    """

    __tablename__ = None
    """The name of the database table this class should be mapped to

    Default: None
    """

    __methods__ = ('GET', 'POST', 'PATCH', 'DELETE', 'PUT')
    """override :attr:`__methods__` if you wish to change the HTTP methods
    this :class:`sandman.model.Model` supports.

    Default: ``('GET', 'POST', 'PATCH', 'DELETE', 'PUT')``
    """

    __table__ = None
    """Will be populated by SQLAlchemy with the table's meta-information."""

    __related_tables__ = set()
    """List of Models for which this model has a foreign key relationship
    with.""" 

    @classmethod
    def endpoint(cls):
        """Return the :class:`sandman.model.Model`'s endpoint.

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
        for foreign_key in self.__table__.foreign_keys:
            column = foreign_key.column.name
            table = foreign_key.column.table.name
            with app.app_context():
                endpoint = current_app.table_to_endpoint[table]
            links.append({'rel': endpoint, 'uri': '/{}/{}'.format(endpoint, getattr(self, column))})
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
        :class:`sandman.model.Model`'s columns.

        :param dict dictionary: A dictionary of attributes to set on the instance
            whose keys are the column names of
            the :class:`sandman.model.Model`'s underlying database table.

        """
        for column in self.__table__.columns.keys():
            value = dictionary.get(column, None)
            if value:
                setattr(self, column, value)

    def replace(self, dictionary):
        """Set all attributes which correspond to the
        :class:`sandman.model.Model`'s columns to the values in *dictionary*,
        inserting None if an attribute's value is not specified.

        :param dict dictionary: A dictionary of attributes to set on the
            instance whose keys are the column names of the
            :class:`sandman.model.Model`'s underlying database table.

        """
        for column in self.__table__.columns.keys():
            setattr(self, column, None)
        self.from_dict(dictionary)

    def __str__(self):
        return str(getattr(self, self.primary_key()))
