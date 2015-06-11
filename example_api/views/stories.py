import logging
from random import random

from nefertari.elasticsearch import ES
from nefertari.view import ESAggregationMixin
from nefertari.json_httpexceptions import (
    JHTTPCreated, JHTTPOk)

from example_api.views.base import BaseView
from example_api.models import Story

log = logging.getLogger(__name__)


class ArbitraryObject(object):
    def __init__(self, *args, **kwargs):
        self.attr = random()

    def to_dict(self, *args, **kwargs):
        return dict(attr=self.attr)


class StoriesView(ESAggregationMixin, BaseView):
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
        try:
            return self.aggregate()
        except KeyError:
            return self.get_collection_es()

    def show(self, **kwargs):
        return self.context

    def create(self):
        story = self.Model(**self._json_params)
        story.arbitrary_object = ArbitraryObject()
        story.save(refresh_index=self.refresh_index)
        pk_field = self.Model.pk_field()

        return JHTTPCreated(
            location=self.request._route_url(
                'stories', getattr(story, pk_field)),
            resource=story.to_dict(),
            request=self.request,
        )

    def update(self, **kwargs):
        pk_field = self.Model.pk_field()
        kwargs = self.resolve_kwargs(kwargs)
        story = self.Model.get_resource(**kwargs)
        story = story.update(
            self._json_params,
            refresh_index=self.refresh_index)

        return JHTTPOk(location=self.request._route_url(
            'stories', getattr(story, pk_field)))

    def replace(self, **kwargs):
        return self.update(**kwargs)

    def delete(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        story = self.Model.get_resource(**kwargs)
        story.delete(refresh_index=self.refresh_index)

        return JHTTPOk()

    def delete_many(self):
        es_stories = self.get_collection_es()
        stories = self.Model.filter_objects(
            es_stories, _limit=self._query_params['_limit'])
        count = self.Model.count(stories)

        if self.needs_confirmation():
            return stories

        self.Model._delete_many(
            stories, refresh_index=self.refresh_index)

        return JHTTPOk("Delete %s %s(s) objects" % (
            count, self.Model.__name__))

    def update_many(self):
        es_stories = self.get_collection_es()
        stories = self.Model.filter_objects(
            es_stories, _limit=self._query_params['_limit'])
        count = self.Model.count(stories)
        self.Model._update_many(
            stories, refresh_index=self.refresh_index,
            **self._json_params)

        return JHTTPOk("Updated %s %s(s) objects" % (
            count, self.Model.__name__))
