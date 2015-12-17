from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    Deny,
    ALL_PERMISSIONS,
    )

from nefertari.acl import (
    CollectionACL,
    authenticated_userid,
    )

from example_api.models import (
    User,
    Story,
    )

from nefertari_guards.acl import DatabaseACLMixin


class UsersACL(CollectionACL):
    item_model = User

    __acl__ = (
        (Allow, 'g:admin', ALL_PERMISSIONS),
        (Allow, Everyone, ('view', 'options')),
        )

    def item_db_id(self, key):
        if key != 'self' or not getattr(self.request, 'user', None):
            return key
        return authenticated_userid(self.request)


class StoriesACL(DatabaseACLMixin, CollectionACL):
    item_model = Story

    __acl__ = (
        (Allow, 'g:admin', ALL_PERMISSIONS),
        (Allow, Everyone, ('view', 'options')),
        (Allow, Authenticated, 'create'),
        )
