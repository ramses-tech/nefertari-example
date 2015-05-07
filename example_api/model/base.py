import logging

from nefertari.elasticsearch import ES as PES
from nefertari.engine import BaseDocument, ESBaseDocument

import example_api


log = logging.getLogger(__name__)


class ES(PES):
    def delete_by_query(self, _q):
        _q = _q or '*'
        self.api.delete_by_query(
            index=self.index_name,
            doc_type=self.doc_type,
            q=_q)


if example_api.Settings.asbool('elasticsearch.index.disable', False):
    log.warning('indexing is TURNED OFF')
    ESBaseDocument = BaseDocument
