import logging

from nefertari.view import BaseView as NefertariBaseView
from nefertari.engine import JSONEncoder
import example_api

log = logging.getLogger(__name__)


class BaseView(NefertariBaseView):
    def __init__(self, context, request, **kw):
        BaseView._json_encoder = JSONEncoder
        super(BaseView, self).__init__(context, request, **kw)

        if self.request.method == 'GET':
            self._query_params.process_int_param('_limit', 20)

        self._auth = example_api.Settings.asbool('auth')

        if '_refresh_index' in self._query_params:
            self.refresh_index = self._query_params.asbool(
                '_refresh_index', pop=True)
        else:
            self.refresh_index = None

    def resolve_kwargs(self, kwargs):
        resolved = {}
        for key, value in kwargs.items():
            key = key.split('_', 1)[1]
            resolved[key] = value
        return resolved
