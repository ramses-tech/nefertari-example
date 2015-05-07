import logging
from random import random

from nefertari.json_httpexceptions import *
from pyramid.security import *

from example_api.views.base import BaseView
from example_api.model import Story
from example_api.model.base import ES

log = logging.getLogger(__name__)


class ArbitraryObject(object):
    def __init__(self, *args, **kwargs):
        self.attr = random()

    def to_dict(self, *args, **kwargs):
        return dict(attr=self.attr)


class StoriesView(BaseView):
    _model_class = Story

    def index(self):
        search_params = []

        if 'q' in self._query_params:
            search_params.append(self._query_params.pop('q'))

        self._raw_terms = ' AND '.join(search_params)

        return ES('Story').get_collection(
            _raw_terms=self._raw_terms,
            **self._query_params)

    def show(self, **kwargs):
        return self.context

    def create(self):
        story = Story(**self._json_params)
        story.arbitrary_object = ArbitraryObject()
        story.save()
        id_field = Story.id_field()
        return JHTTPCreated(location=self.request._route_url(
            'stories', getattr(story, id_field)))

    def update(self, **kwargs):
        id_field = Story.id_field()
        kwargs = self.resolve_kwargs(kwargs)
        story = Story.get_resource(**kwargs).update(self._json_params)
        return JHTTPOk(location=self.request._route_url(
            'stories', getattr(story, id_field)))

    def delete(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        Story._delete(**kwargs)
        return JHTTPOk()

    def delete_many(self):
        stories = Story.get_collection(**self._query_params)
        count = Story.count(stories)

        if self.needs_confirmation():
            return stories

        Story._delete_many(stories)

        return JHTTPOk("Delete %s %s(s) objects" % (
            count, self._model_class.__name__))

    def update_many(self):
        self._query_params.process_int_param('_limit', 1000)
        stories = Story.get_collection(**self._query_params)
        count = Story.count(stories)
        Story._update_many(stories, **self._json_params)

        return JHTTPOk("Updated %s %s(s) objects" % (
            count, self._model_class.__name__))
