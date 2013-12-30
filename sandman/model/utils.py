"""Various utility functions for registering and activating models."""
import webbrowser

from flask import current_app
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

from sandman import app, db
from sandman.model.models import Model, AdminModelViewWithPK

def generate_models():
    """Return a list of model classes generated for each reflected database
    table."""
    classes = {}
    with app.app_context():
        db.metadata.reflect(bind=db.engine)
        for name, table in db.metadata.tables.items():
            cls_dict = {'__tablename__': name}
            if not table.primary_key and current_app.config[
                    'SANDMAN_ALL_PRIMARY']:
                cls = generate_primary_key(table)
            else:
                cls = type(str(name), (sandman_model, db.Model), cls_dict)
            register(cls)
            classes[cls.endpoint()] = cls
    return classes

def generate_primary_key(table):
    """Return a class deriving from our Model class as well as the SQLAlchemy
    model.

    :param `sqlalchemy.schema.Table` table: table to create primary key for

    """
    with app.app_context():
        db.metadata.reflect(bind=db.engine)
        for name, table in db.metadata.tables.items():
            cls_dict = {'__tablename__': name}
            if not table.primary_key and current_app.config[
                    'SANDMAN_ALL_PRIMARY']:
                for column in table.columns:
                    column.primary_key = True
                Table(name, db.metadata, *table.columns, extend_existing=True)
                cls_dict['__table__'] = table
                db.metadata.create_all(bind=db.engine)

            return type(str(name), (sandman_model, db.Model), cls_dict)

def prepare_relationships(app_handle):
    """Enrich the registered Models with SQLAlchemy ``relationships``
    so that related tables are correctly processed up by the admin.

    """
    inspector = reflection.Inspector.from_engine(db.engine)
    with app_handle.app_context():
        for cls in current_app.classes:
            for foreign_key in inspector.get_foreign_keys(cls.__tablename__):
                other = current_app.classes_by_name[
                        foreign_key['referred_table']]
                cls.__related_tables__.add(other)
                # Add a SQLAlchemy relationship as an attribute on the class
                setattr(cls, other.__name__.lower(), relationship(
                    other.__name__, backref=cls.__name__))

def register(cls, use_admin=True):
    """Register with the API a :class:`sandman.model.Model` class and associated
    endpoint.

    :param cls: User-defined class derived from :class:`sandman.model.Model` to
                be registered with the endpoint returned by :func:`endpoint()`
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
                register_internal_data(entry)
                entry.use_admin = use_admin
        else:
            register_internal_data(cls)
            cls.use_admin = use_admin

def register_internal_data(cls):
    """Register a new class, *cls*, with various internal data structures.

    :params `sandman.model.Model` cls: class to register

    """
    with app.app_context():
        current_app.endpoint_classes[cls.endpoint()] = cls
        current_app.table_to_endpoint[cls.__tablename__] = cls.endpoint()
        current_app.classes_by_name[cls.__tablename__] = cls
        current_app.classes.append(cls)
        cls.__related_tables__ = set()

def register_classes_for_admin(app_handle, db_session, classes, show_pks=True,
        name='admin'):
    """Registers classes for the Admin view that ultimately creates the admin
    interface.

    :param app_handle: handle to flask application
    :param db_session: handle to database session
    :param list classes: list of classes to register with the admin
    :param bool show_pks: show primary key columns in the admin?

    """

    print name
    admin_view = Admin(app_handle, endpoint=name)
    with app_handle.app_context():
        for cls in (cls for cls in classes if
                cls.use_admin == True):
            if show_pks:
                # the default of Flask-SQLAlchemy is to not show primary
                # classes, which obviously isn't acceptable in some cases
                column_list = [
                        column.name for column in
                        cls.__table__.columns.values()]
                admin_view_class = type('AdminView', (AdminModelViewWithPK,),
                        {'form_columns': column_list})
                admin_view.add_view(admin_view_class(cls, db_session))
            else:
                admin_view.add_view(ModelView(cls, db_session))

def activate(admin=True, browser=True, name='admin'):
    """Activate each pre-registered model or generate the model classes and
    (possibly) register them for the admin.

    :param bool admin: should we generate the admin interface?
    :param bool browser: should we open the browser for the user?
    :param name: name to use for blueprint created by the admin interface. Set
                 this to avoid naming conflicts with other blueprints (if trying
                 to use sandman to connect to multiple databases simultaneously)

    """
    with app.app_context():
        if getattr(current_app, 'endpoint_classes', None) is None:
            current_app.endpoint_classes = generate_models()
        else:
            Model.prepare(db.engine)
        prepare_relationships(current_app)
        if admin:
            register_classes_for_admin(current_app, db.session,
                current_app.classes,
                current_app.config['SANDMAN_SHOW_PKS'],
                name)
    if browser:
        webbrowser.open('http://127.0.0.1:5000/admin')

# Redefine 'Model' to be a sqlalchemy.ext.declarative.api.DeclarativeMeta
# object which also derives from sandman.models.Model. The naming is done for
# documentation/clarity purposes. Previously the line below had Model deriving
# from DeferredReflection and "Resource", which was the exact same class
# as "Model" in models.py. It caused confusion in the documentation, however,
# since it wasn't clear that the Model class and the Resource class were
# actually the same thing.

sandman_model = Model
Model = declarative_base(cls=(Model, DeferredReflection))
