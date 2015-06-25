import logging
from random import random

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

    def index(self):
        return self.get_collection_es()

    def show(self, **kwargs):
        return self.context

    def create(self):
        story = self.Model(**self._json_params)
        story.arbitrary_object = ArbitraryObject()
        return story.save(refresh_index=self.refresh_index)

    def update(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        story = self.Model.get_resource(**kwargs)
        return story.update(
            self._json_params,
            refresh_index=self.refresh_index)

    def replace(self, **kwargs):
        return self.update(**kwargs)

    def delete(self, **kwargs):
        kwargs = self.resolve_kwargs(kwargs)
        story = self.Model.get_resource(**kwargs)
        story.delete(refresh_index=self.refresh_index)

    def delete_many(self):
        es_stories = self.get_collection_es()
        stories = self.Model.filter_objects(
            es_stories, _limit=self._query_params['_limit'])

        if self.needs_confirmation():
            return stories

        return self.Model._delete_many(
            stories, refresh_index=self.refresh_index)

    def update_many(self):
        es_stories = self.get_collection_es()
        stories = self.Model.filter_objects(
            es_stories, _limit=self._query_params['_limit'])

        return self.Model._update_many(
            stories, refresh_index=self.refresh_index,
            **self._json_params)
