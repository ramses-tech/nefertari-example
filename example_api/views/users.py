import logging

from example_api.views.base import BaseView
from example_api.models import User, Profile


log = logging.getLogger(__name__)


class UsersView(BaseView):
    Model = User

    def index(self):
        if 'groups' not in self._query_params:
            self._query_params['groups'] = 'user'
        elif self._query_params['groups'] == '_all':
            self._query_params.pop('groups')
        return self.Model.get_collection(**self._query_params)

    def show(self, **kwargs):
        return self.context

    def create(self):
        self._json_params.setdefault('groups', ['user'])
        user = self.Model(**self._json_params)
        return user.save()

    def update(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        user = self.Model.get_resource(**kwargs)

        # empty password?
        if 'password' in self._json_params and \
                self._json_params['password'] == '':
            self._json_params.pop('password')

        if 'reset' in self._json_params:
            self._json_params.pop('reset', '')
        return user.update(self._json_params)

    def replace(self, **kwargs):
        return self.update(**kwargs)

    def delete(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        story = self.Model.get_resource(**kwargs)
        story.delete()


class UserAttributesView(BaseView):
    Model = User

    def __init__(self, *args, **kw):
        super(UserAttributesView, self).__init__(*args, **kw)
        self.attr = self.request.path.split('/')[-1]
        self.value_type = None
        self.unique = self.attr in ['settings', 'groups']

    def index(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        obj = self.Model.get_resource(**kwargs)
        return getattr(obj, self.attr)

    def create(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        obj = self.Model.get_resource(**kwargs)
        obj.update_iterables(
            self._json_params, self.attr,
            unique=self.unique,
            value_type=self.value_type)
        return getattr(obj, self.attr, None)


class UserProfileView(BaseView):
    Model = Profile

    def show(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        user = User.get_resource(**kwargs)
        return user.profile

    def create(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        obj = User.get_resource(**kwargs)
        profile = self.Model(**self._json_params)
        profile = profile.save()
        obj.update({'profile': profile})
        return obj.profile

    def update(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        user = User.get_resource(**kwargs)
        return user.profile.update(self._json_params)

    def replace(self, **kwargs):
        return self.update(**kwargs)
