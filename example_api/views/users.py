import logging
from pyramid.security import *
from nefertari.json_httpexceptions import *

from example_api.views.base import BaseView
from example_api.model import User


log = logging.getLogger(__name__)


class UsersView(BaseView):
    _model_class = User

    def index(self):
        if 'groups' not in self._params:
            self._params['groups'] = 'user'
        elif self._params['groups'] == '_all':
            self._params.pop('groups')
        return self._model_class.get_collection(**self._params)

    def show(self, **kwargs):
        return self.context

    def create(self):
        self._params.setdefault('groups', ['user'])

        user = self._model_class(**self._params).save()
        id_field = self._model_class.id_field()

        return JHTTPCreated(
            location=self.request._route_url('users', getattr(user, id_field)),
            resource=user.to_dict(request=self.request))

    def update(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        user = self._model_class.get_resource(**kwargs)

        # empty password?
        if 'password' in self._params and self._params['password'] == '':
            self._params.pop('password')

        if 'reset' in self._params:
            self._params.pop('reset', '')
        user.update(self._params)

        id_field = self._model_class.id_field()
        return JHTTPOk(location=self.request._route_url(
            'users', getattr(user, id_field)))

    def delete(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        self._model_class._delete(**kwargs)
        return JHTTPOk()


class UserAttributesView(BaseView):
    _model_class = User

    def __init__(self, *args, **kw):
        super(UserAttributesView, self).__init__(*args, **kw)
        self.attr = self.request.path.split('/')[-1]
        self.value_type = None
        self.unique = self.attr in ['settings', 'groups']

    def index(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        obj = self._model_class.get_resource(**kwargs)
        return getattr(obj, self.attr)

    def create(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        obj = self._model_class.get_resource(**kwargs)
        obj.update_iterables(
            self._params, self.attr,
            unique=self.unique,
            value_type=self.value_type)
        return JHTTPCreated(resource=getattr(obj, self.attr, None))


class UserProfileView(BaseView):
    _model_class = Profile

    def index(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        obj = self._model_class.get_resource(**kwargs)
        return getattr(obj, self.attr)

    def create(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        obj = self._model_class.get_resource(**kwargs)
        obj.profile = _model_class(self._params)
        return JHTTPCreated(resource=obj.profile)

    def update(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        user = self._model_class.get_resource(**kwargs)
        user.profile.update(self._params)

        id_field = self._model_class.id_field()
        return JHTTPOk(location=self.request._route_url(
            'users:profile', getattr(user, id_field)))
