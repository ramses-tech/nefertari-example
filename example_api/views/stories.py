import logging
from random import random

from nefertari.elasticsearch import ES

from example_api.views.base import BaseView
from example_api.models import Story

log = logging.getLogger(__name__)


class ArbitraryObject(object):
    def __init__(self, *args, **kwargs):
        self.attr = random()

    def to_dict(self, *args, **kwargs):
        return dict(attr=self.attr)


class StoriesView(BaseView):
    Model = Story

    def get_collection_es(self):
        search_params = []

        if 'q' in self._query_params:
            search_params.append(self._query_params.pop('q'))

        self._raw_terms = ' AND '.join(search_params)

        return ES(self.Model.__name__).get_collection(
            _raw_terms=self._raw_terms,
            **self._query_params)

    def index(self):
        return self.get_collection_es()

    def show(self, **kwargs):
        return self.context

    def create(self):
        story = self.Model(**self._json_params)
        story.arbitrary_object = ArbitraryObject()
        return story.save(self._query_params)

    def update(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        story = self.Model.get_resource(**kwargs)
        return story.update(self._json_params, self._query_params)

    def replace(self, **kwargs):
        return self.update(**kwargs)

    def delete(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        story = self.Model.get_resource(**kwargs)
        story.delete(self._query_params)

    def delete_many(self):
        es_stories = self.get_collection_es()
        stories = self.Model.filter_objects(
            es_stories, _limit=self._query_params['_limit'])

        if self.needs_confirmation():
            return stories

        return self.Model._delete_many(stories, self._query_params)

    def update_many(self):
        es_stories = self.get_collection_es()
        stories = self.Model.filter_objects(
            es_stories, _limit=self._query_params['_limit'])

        return self.Model._update_many(
            stories, self._json_params, self._query_params)
