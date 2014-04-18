==============
Authentication
==============

``sandman`` supports HTTP basic authentication, meaning a username and password
must be passed on each request via the ``Authorization`` header. 

Enabling Authentication
-----------------------

Enabling authentication in your ``sandman`` installation is a straight-forward task.
You'll need to define two functions:

* ``get_password()``
* ``before_request()``

The former is required by ``Flask-HTTPAuth``, which powers ``sandman's``
authentication. The latter is used to ensure that _all_ requests are authorized.

``get_password``
~~~~~~~~~~~~~~~~

The ``get_password`` function takes a ``username`` as an argument and should
return the associated password for that user. To notify Flask-HTTPAuth that this
is the function responsible for returning passwords, it must be wrapped with the 
``@auth.get_password`` decorator (``auth`` is importable from ``sandman``, e.g.
``from sandman import app, db, auth``). How you implement your user
management system is up to you; you simply need to implement ``get_password`` in
whatever way is most appropriate for your security setup.

As a trivial example, here's an implementation of ``get_password`` that always
returns ``secret``, meaning ``secret`` must be the password, regardless of
the ``username``::

    @auth.get_password
    def get_password(username):
        """Return the password for *username*."""
        return 'secret'

``before_request``
~~~~~~~~~~~~~~~~~~

Once you've hooked up your password function, it's time to tell Flask which
requests should require authentication. Rather than picking and choosing on a
request by request basis, we use the ``@app.before_request`` decorator included
in Flask to make sure _all_ requests are authenticated. Here's a sample
implementation::

    @app.before_request
    @auth.login_required
    def before_request():
        pass

Notice the function just calls ``pass``; it needn't have any logic, since the
logic is added by Flask-HTTPAuth's ``@auth.login_required`` decorator.

Token-based Authentication
--------------------------

There are plans for ``sandman`` to support token-based authentication, but this
currently isn't supported and no time frame for implementation has been set.
