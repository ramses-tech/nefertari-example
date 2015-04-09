import logging

from nefertari.json_httpexceptions import *
from nefertari.view import BaseView as NefertariBaseView
from nefertari.engine import JSONEncoder
import example_api

log = logging.getLogger(__name__)


class BaseView(NefertariBaseView):
    def __init__(self, context, request, **kw):
        BaseView._json_encoder = JSONEncoder
        super(BaseView, self).__init__(context, request, **kw)

        if self.request.method == 'GET':
            self._params.process_int_param('_limit', 20)

        self._params.process_datetime_param('timestamp')
        self._auth = example_api.Settings.asbool('auth')

    def resolve_kwargs(self, kwargs):
        resolved = {}
        for key, value in kwargs.items():
            key = key.split('_', 1)[1]
            if value == 'self':
                value = getattr(self.request.user, key)
            resolved[key] = value
        return resolved
