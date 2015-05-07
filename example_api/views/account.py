import logging

from pyramid.security import remember, forget
from nefertari.json_httpexceptions import *

from example_api.model import User
from example_api.views.base import BaseView

log = logging.getLogger(__name__)


class AccountView(BaseView):
    _model_class = User

    def create(self):
        user, created = User.create_account(self._params)

        def login():
            if not user.verify_password(self._params['password']):
                raise JHTTPConflict('Looks like you already have an account.'
                    ' <a href="/login?email=%s">Login here</a>.' % user.email)

            return self.login(login=user.email, password=self._params['password'])

        if user.is_active():
            return login()

        user.status = 'active'
        user.save()
        return login()

    def login(self, **params):
        self._params.update(params)
        next = self._params.get('next', '')
        login_url = self.request.route_url('login')
        if next.startswith(login_url):
            next = '' # never use the login form itself as next

        unauthorized_url = self._params.get('unauthorized', None)
        success, user = User.authenticate(self._params)

        if success:
            if user and user.status in ['blocked', 'inactive']:
                raise JHTTPUnauthorized('User %s is %s' % (user.email, user.status))

            headers = remember(self.request, user.uid)
            user.on_login(self.request)
            if next:
                raise JHTTPFound(location=next, headers=headers)
            else:
                return JHTTPOk(headers=headers)
        if user:
            if unauthorized_url:
                return JHTTPUnauthorized(location=unauthorized_url+'?error=1')

            raise JHTTPUnauthorized('Failed to Login.')
        else:
            raise JHTTPNotFound('user not found')

    def logout(self):
        next = self._params.get('next', '/')
        headers = forget(self.request)
        return JHTTPFound(location=next, headers=headers)
