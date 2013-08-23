"""The model module is repsonsible exposes the :class:`sandman.model.Model` class,
from which user models should derive. It also makes the :func:`register`
function available, which maps endpoints to their associated classes."""

from .models import Model
from .. import db, app
from flask import current_app
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

def register(cls, use_admin=True):
    """Register with the API a :class:`sandman.model.Model` class and associated
    endpoint.

    :param cls: User-defined class derived from :class:`sandman.model.Model` to be
                registered with the endpoint returned by :func:`endpoint()`
    :type cls: :class:`sandman.model.Model` or tuple

    """
    with app.app_context():
        if getattr(current_app, 'endpoint_classes', None) is None:
            current_app.endpoint_classes = {}
            current_app.classes_by_name = {}
            current_app.table_to_endpoint = {}
        if isinstance(cls, (list, tuple)):
            for entry in cls:
                _register_internal_data(entry)
                entry.use_admin = use_admin
        else:
            _register_internal_data(cls)
            cls.use_admin = use_admin
    Model.prepare(db.engine)

def _register_internal_data(cls):
    with app.app_context():
        current_app.endpoint_classes[cls.endpoint()] = cls
        current_app.table_to_endpoint[cls.__tablename__] = cls.endpoint()
        current_app.classes_by_name[cls.__name__] = cls

def _prepare_relationships():
    """Enrich the registered Models with SQLAlchemy ``relationships``
    so that related tables are correctly processed up by the admin."""
    inspector = reflection.Inspector.from_engine(db.engine)
    with app.app_context():
        for cls in current_app.classes_by_name.values():
            for foreign_key in inspector.get_foreign_keys(cls.__tablename__):
                other = current_app.classes_by_name[foreign_key['referred_table']]
                other.__related_tables__.add(cls)
                cls.__related_tables__.add(other)
                # Necessary to get Flask-Admin to register the relationship
                setattr(other, '_ref_' + cls.__tablename__.lower(), relationship(cls.__tablename__, backref='_fk_' + other.__tablename__.lower()))

def activate_admin_classes():
    """Activate each registed Model in the admin if it was registered with
    *use_admin=True*."""
    _prepare_relationships()
    admin = Admin(app)
    with app.app_context():
        for cls in (cls for cls in current_app.classes_by_name.values() if cls.use_admin == True):
            admin.add_view(ModelView(cls, db.session))


# Redefine 'Model' to be a sqlalchemy.ext.declarative.api.DeclarativeMeta
# object which also derives from sandman.models.Model. The naming is done for
# documentation/clarity purposes. Previously the line below had Model deriving
# from DeferredReflection and "Resource", which was the exact same class
# as "Model" in models.py. It caused confusion in the documentation, however,
# since it wasn't clear that the Model class and the Resource class were
# actually the same thing.
Model = declarative_base(cls=(Model, DeferredReflection))
