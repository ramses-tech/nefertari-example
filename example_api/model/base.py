import logging

from nefertari.elasticsearch import ES as PES
from nefertari.engine import BaseDocument as NefertariBaseDocument
from nefertari.engine import ESBaseDocument as NefertariESBaseDocument

import example_api


log = logging.getLogger(__name__)


class ES(PES):
    def delete_by_query(self, _q):
        _q = _q or '*'
        self.api.delete_by_query(
            index=self.index_name,
            doc_type=self.doc_type,
            q=_q)


class BaseDocumentMixin(object):

    def to_dict(self, **kw):
        _dict = super(BaseDocumentMixin, self).to_dict(**kw)

        request = kw.get('request', None)
        _nested = kw.get('__nested', False)
        _fields = set(_dict.keys())

        if request and request.user:
            if not request.user.is_admin() and self._auth_fields:
                _fields &= set(self._auth_fields)

        if _nested and self._nested_fields:
            _fields &= set(self._nested_fields)

        if _fields:
            _fields.add('_type')
            _dict = _dict.subset(_fields)
        return _dict


class BaseDocument(BaseDocumentMixin, NefertariBaseDocument):
    __abstract__ = True
    meta = {
        'abstract': True,
    }


class ESBaseDocument(BaseDocumentMixin, NefertariESBaseDocument):
    """ Inherit custom ``to_dict`` """
    __abstract__ = True
    meta = {
        'abstract': True,
    }


if example_api.Settings.asbool('elasticsearch.index.disable', False):
    log.warning('indexing is TURNED OFF')
    ESBaseDocument = BaseDocument
