import logging

from nefertari.utils import to_dicts
from nefertari.elasticsearch import ES

from example_api.views.base import BaseView

log = logging.getLogger(__name__)


class SView(BaseView):
    def index(self):
        q = self._params.pop('q', None)
        if not q:
            return []

        return to_dicts(ES().get_collection(
            q='name:%s*' % (q,), _limit=5,
        ), _keys=['id', 'name'])
