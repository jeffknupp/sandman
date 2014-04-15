from sandman import auth, app

@auth.get_password
def get_password(username):
    """Return the password associated with the user *username*."""
    raise NotImplementedError('You must implement \'get_password\' to enable authentication.')

@app.before_request
@auth.login_required
@rate_limit(5, 5)
def before_request():
    pass
