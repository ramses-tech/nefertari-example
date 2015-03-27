from pyramid.security import *

from nefertari.json_httpexceptions import *
from nefertari.acl import BaseACL as NefertariBaseACL, AuthenticatedUserACLMixin
from example_api.model import User, Story


class BaseACL(NefertariBaseACL):
    def __init__(self, request):
        super(BaseACL, self).__init__(request)

        username = request.matchdict.get('username')
        if username and username != 'self':
            self.user = User.get(username=username, __raise=True)
        else:
            self.user = request.user


class UserACL(AuthenticatedUserACLMixin, BaseACL):
    __context_class__ = User


class StoryACL(BaseACL):
    __context_class__ = Story

    def __init__(self, request):
        super(StoryACL, self).__init__(request)
        self.acl = (Allow, Everyone, ['index', 'show'])

    def context_acl(self, context):
        return [
            (Allow, 'g:admin', ALL_PERMISSIONS),
            (Allow, Everyone, ['index', 'show']),
        ]

    def __getitem__(self, key):
        obj = Story.get(id=key, __raise=True)
        obj.__acl__ = self.context_acl(obj)
        obj.__parent__ = self
        obj.__name__ = key
        return obj
