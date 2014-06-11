"""Admin for Sandman."""

from flask import Blueprint, request, render_template, flash
from flask.views import MethodView

from sandman import db


class Admin():

    def __init__(self, app, endpoint='/admin', name='admin'):
        self._endpoint = endpoint
        self._name = name
        self.blueprint = Blueprint(self._endpoint, name)
        self.blueprint.add_url_rule(self._endpoint, view_func=self.home)
        self._model_classes = []

    def register(self, cls):
        """Register a class to be given a REST API."""
        cls.__admin__ = self
        self._model_classes.append(cls)
        view_func = cls.as_view(
            cls.__model__.__tablename__)
        self.blueprint.add_url_rule(
            self._endpoint + '/' + cls.__model__.__tablename__.lower(),
            view_func=view_func)

    def home(self):
        return render_template('admin/base.html')


class AdminModel(MethodView):
    """Base class for all resources."""

    __model__ = None
    __admin__ = None

    def get(self, resource_id=None):
        """Return response to HTTP GET request."""
        if resource_id is None:
            return render_template(
                'admin/collection.html',
                resources=self._all_resources(), admin=self.__admin__)
        else:
            resource = self._resource(resource_id)
            if not resource:
                return render_template('admin/404.html', admin=self.__admin__)
            return render_template(
                'admin/edit_resource.html',
                resource=resource, admin=self.__admin__)

    def _all_resources(self):
        """Return all resources of this type as a JSON list."""
        if not 'page' in request.args:
            page = 1
        else:
            page = request.args['page']
        return db.session.query(self.__model__).offset(page).limit(20)

    def post(self):
        """Return response to HTTP POST request."""
        # pylint: disable=unused-argument
        # resource already exists; don't create it again
        resource = self.__model__(  # pylint: disable=not-callable
            **request.form)
        db.session.add(resource)
        db.session.commit()
        flash('Successfully created')
        return render_template(
            'admin/collection.html',
            resources=self._all_resources(), admin=self.__admin__)

    def delete(self, resource_id):
        """Return response to HTTP DELETE request."""
        resource = self._resource(resource_id)
        db.session.delete(resource)
        db.session.commit()
        flash('Successfully deleted')
        return render_template(
            'admin/collection.html',
            resources=self._all_resources(), admin=self.__admin__)

    def put(self, resource_id):
        """Return response to HTTP PUT request."""
        resource = self._resource(resource_id)
        if resource is None:
            resource = self.__model__(   # pylint: disable=not-callable
                **request.json)
        else:
            resource.from_dict(request.json)
        db.session.add(resource)
        db.session.commit()
        return render_template('admin/collection', resource=resource,
                admin=self.__admin__)

    def _resource(self, resource_id):
        """Return resource represented by this *resource_id*."""
        resource = db.session.query(self.__model__).get(resource_id)
        if not resource:
            return None
        return resource
