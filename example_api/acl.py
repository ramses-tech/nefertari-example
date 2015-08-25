from pyramid.security import (
    Allow,
    Everyone,
    Deny,
    ALL_PERMISSIONS,
    )

from nefertari.acl import (
    ContainerACL,
    ItemACL,
    authenticated_userid,
    )

from example_api.models import (
    User,
    Story,
    )


class UserACL(ItemACL):
    db_class = User

    def db_key(self, key):
        if key != 'self' or not self.request.user:
            return key
        return authenticated_userid(self.request)

    def custom_acl(self):
        username = str(self.db_object().username)
        return (
            (Allow, 'g:admin', ALL_PERMISSIONS),
            (Allow, Everyone, ('view', 'options')),
            (Allow, username, 'update'),
            (Deny, username, 'delete'),
            )


class UsersACL(ContainerACL):
    child_class = UserACL
    __acl__ = (
        (Allow, 'g:admin', ALL_PERMISSIONS),
        (Allow, Everyone, ('view', 'create', 'options')),
        )


class StoriesACL(ContainerACL):
    __acl__ = (
        (Allow, 'g:admin', ALL_PERMISSIONS),
        (Allow, Everyone, ('view', 'create', 'options')),
        )
