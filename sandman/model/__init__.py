"""The model module is repsonsible exposes the :class:`sandman.model.Model` class,
from which user models should derive. It also makes the :func:`register`
function available, which maps endpoints to their associated classes."""

from .models import Model
from .. import db, app
from flask import current_app
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection

def register(cls):
    """Register with the API a :class:`sandman.model.Model` class and associated
    endpoint.

    :param cls: User-defined class derived from :class:`sandman.model.Model` to be
                registered with the endpoint returned by :func:`endpoint()`
    :type cls: :class:`sandman.model.Model` or tuple

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

# Redefine 'Model' to be a sqlalchemy.ext.declarative.api.DeclarativeMeta
# object which also derives from sandman.models.Model. The naming is done for
# documentation/clarity purposes. Previously the line below had Model deriving
# from DeferredReflection and "Resource", which was the exact same class
# as "Model" in models.py. It caused confusion in the documentation, however,
# since it wasn't clear that the Model class and the Resource class were
# actually the same thing.
Model = declarative_base(cls=(Model, DeferredReflection))
