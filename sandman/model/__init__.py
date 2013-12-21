"""The model module is repsonsible exposes the :class:`sandman.model.Model` class,
from which user models should derive. It also makes the :func:`register`
function available, which maps endpoints to their associated classes."""

import webbrowser

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
            current_app.classes = []
        if isinstance(cls, (list, tuple)):
            for entry in cls:
                _register_internal_data(entry)
                entry.use_admin = use_admin
        else:
            _register_internal_data(cls)
            cls.use_admin = use_admin

def _register_internal_data(cls):
    with app.app_context():
        current_app.endpoint_classes[cls.endpoint()] = cls
        current_app.table_to_endpoint[cls.__tablename__] = cls.endpoint()
        current_app.classes_by_name[cls.__tablename__] = cls
        current_app.classes.append(cls)

def _prepare_relationships():
    """Enrich the registered Models with SQLAlchemy ``relationships``
    so that related tables are correctly processed up by the admin."""
    inspector = reflection.Inspector.from_engine(db.engine)
    with app.app_context():
        for cls in current_app.classes:
            for foreign_key in inspector.get_foreign_keys(cls.__tablename__):
                other = current_app.classes_by_name[foreign_key['referred_table']]
                if other==cls:
                    continue
                other.__related_tables__.add(cls)
                cls.__related_tables__.add(other)
                # Necessary to get Flask-Admin to register the relationship
                setattr(other, '__' + cls.__name__.lower(), relationship(cls.__name__, backref=other.__name__.lower()))

def activate(admin=True):
    """Activate each registered model for non-admin use"""
    with app.app_context():
        if getattr(current_app, 'endpoint_classes', None) is None:
            current_app.endpoint_classes = {}
            current_app.classes_by_name = {}
            current_app.table_to_endpoint = {}
            current_app.classes = []
        if not current_app.endpoint_classes:
            db.metadata.reflect(bind=db.engine)
            for name, table in db.metadata.tables.items():
                try:
                    cls = type(str(name), (sandman_model, db.Model), {'__tablename__': name})
                    register(cls)
                except:
                    print name + ' unable to be registered'
        else:
            Model.prepare(db.engine)
    if admin:
        _prepare_relationships()
        admin = Admin(app)
        with app.app_context():
            for cls in (cls for cls in current_app.classes if cls.use_admin == True):
                admin.add_view(ModelView(cls, db.session))
    webbrowser.open('http://localhost:5000/admin')


# Redefine 'Model' to be a sqlalchemy.ext.declarative.api.DeclarativeMeta
# object which also derives from sandman.models.Model. The naming is done for
# documentation/clarity purposes. Previously the line below had Model deriving
# from DeferredReflection and "Resource", which was the exact same class
# as "Model" in models.py. It caused confusion in the documentation, however,
# since it wasn't clear that the Model class and the Resource class were
# actually the same thing.
sandman_model = Model
Model = declarative_base(cls=(Model, DeferredReflection))
