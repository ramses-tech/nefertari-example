import logging
from pyramid.security import *
from nefertari.json_httpexceptions import *

from example_api.views.base import BaseView
from example_api.model import User


log = logging.getLogger(__name__)


class UsersView(BaseView):
    _model_class = User

    def index(self):
        if 'group' not in self._params:
            self._params['group'] = 'user'
        elif self._params['group'] == '_all':
            self._params.pop('group')
        return User.get_collection(**self._params)

    def show(self, username):
        return self.context

    def create(self):
        self._params.setdefault('group', 'user')

        user = User(**self._params).save()

        return JHTTPCreated(
            location=self.request._route_url('users', user.username),
            resource=user.to_dict(request=self.request))

    def update(self, username):
        user = User.get_resource(username=username)

        if 'group' in self._params:
            raise JHTTPBadRequest('Use User attributes resource to modify `group`')

        # empty password?
        if 'password' in self._params and self._params['password'] == '':
            self._params.pop('password')

        if 'reset' in self._params:
            self._params.pop('reset', '')
        user.update(self._params)

        return JHTTPOk()

    def delete(self, username):
        User._delete(username=username)
        return JHTTPOk()


class UserAttributesView(BaseView):
    def __init__(self, *args, **kw):
        super(UserAttributesView, self).__init__(*args, **kw)
        self.attr = self.request.path.split('/')[-1]
        self.attr = self.attr[:-1] if self.attr.endswith('s') else self.attr
        self.value_type = None

        self.unique = self.attr in ['group']

        if self.attr == 'group':
            self.value_type = str

    def index(self, username):
        user = User.get_resource(username=username)
        return getattr(user, self.attr)

    def create(self, username):
        obj = User.get_resource(username=username)
        obj.group = self._params.get(self.attr)
        obj.save()
        return JHTTPCreated()
