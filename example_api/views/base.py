import logging

from nefertari.json_httpexceptions import *
from nefertari.view import BaseView as NefertariBaseView
from nefertari.engine import JSONEncoder
import example_api
from example_api.model import User

log = logging.getLogger(__name__)


class BaseView(NefertariBaseView):
    def __init__(self, context, request, **kw):
        BaseView._json_encoder = JSONEncoder
        super(BaseView, self).__init__(context, request, **kw)

        if self.request.method == 'GET':
            self._params.process_int_param('_limit', 20)

        self._params.process_datetime_param('timestamp')
        self._auth = example_api.Settings.asbool('auth')

    def is_admin(self):
        if not self._auth:
            return True

        if self._auth and self.request.user:
            return self.request.user.is_admin()
        else:
            return False
        return True

    def set_owner(self):
        req = self.request
        if 'username' in req.matchdict:
            if req.user and req.user.username == req.matchdict['username']:
                self._params['owner'] = req.user
            else:
                self._params['owner'] = User.get(
                    username=req.matchdict['username'])
