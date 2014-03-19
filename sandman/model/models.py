"""The Model class is meant to be the base class for user Models. It represents
a table in the database that should be modeled as a resource."""

from decimal import Decimal

from flask import current_app
from flask.ext.admin.contrib.sqla import ModelView

from sandman import app, db


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

    @classmethod
    def endpoint(cls):
        """Return the :class:`sandman.model.Model`'s endpoint.

        :rtype: string

        """
        if cls.__endpoint__ is not None:
            return cls.__endpoint__
        value = cls.__tablename__.lower()
        if not value.endswith('s'):
            value += 's'
        return value

    def resource_uri(self):
        """Return the URI at which the resource can be found.

        :rtype: string

        """
        primary_key_value = getattr(self, self.primary_key(), None)
        return '/{}/{}'.format(self.endpoint(), primary_key_value)

    @classmethod
    def primary_key(cls):
        """Return the name of the table's primary key

        :rtype: string

        """

        return cls.__table__.primary_key.columns.values()[0].name

    def as_dict(self, depth=1):
        """Return a dictionary containing only the attributes which map to
        an instance's database columns.

        :rtype: dict

        """
        result_dict = {}
        for column in self.__table__.columns.keys():
            result_dict[column] = getattr(self, column, None)
            if isinstance(result_dict[column], Decimal):
                result_dict[column] = str(result_dict[column])
        for foreign_key in self.__table__.foreign_keys:
            column_name = foreign_key.column.name
            column_value = getattr(self, column_name, None)
            if column_value:
                table = foreign_key.column.table.name
                with app.app_context():
                    endpoint = current_app.class_references[table]
                    session = db.session()
                    resource = session.query(endpoint).get(column_value)
                if depth < 2:
                    result_dict.update({
                        'rel': endpoint.__name__, 
                        endpoint.__name__.lower() + ':' : resource.as_dict(depth + 1)
                        })
                else:
                    result_dict[endpoint.__name__.lower() + '_url'] = '/{}/{}'.format(endpoint.__name__, column_value)

        result_dict['self'] = self.resource_uri()
        return result_dict

    def from_dict(self, dictionary):
        """Set a set of attributes which correspond to the
        :class:`sandman.model.Model`'s columns.

        :param dict dictionary: A dictionary of attributes to set on the
            instance whose keys are the column names of
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

class AdminModelViewWithPK(ModelView):
    """Mixin admin view class that displays primary keys on the admin form"""
    column_display_pk = True

class AuthenticatedAdminModelView(ModelView):

    def is_accessible(self):
        raise NotImplementedError('You must implement the \'is_accessible\' method to use authorization.')
