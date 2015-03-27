import logging
from nefertari.json_httpexceptions import *
from pyramid.security import *

from example_api.views.base import BaseView
from example_api.model import Story
from example_api.model.base import ES

log = logging.getLogger(__name__)


class StoriesView(BaseView):
    _model_class = Story

    def index(self):
        search_params = []

        if 'q' in self._params:
            search_params.append(self._params.pop('q'))

        self._raw_terms = ' AND '.join(search_params)

        return ES('Story').get_collection(
            _raw_terms=self._raw_terms,
            **self._params)

    def show(self, id):
        return self.context

    def create(self):
        story = Story(**self._params)
        story.save()
        return JHTTPCreated(
            location=self.request._route_url('stories', story.id))

    def update(self, id):
        story = Story.get_resource(id=id).update(self._params)
        return JHTTPOk(location=self.request._route_url('stories', story.id))

    def delete(self, id):
        Story._delete(id=id)
        return JHTTPOk()

    def delete_many(self):
        stories = Story.get_collection(**self._params)
        count = stories.count()

        if self.needs_confirmation():
            return stories

        Story._delete_many(stories)

        return JHTTPOk("Delete %s %s(s) objects" % (
            count, self._model_class.__name__))

    def update_many(self):
        _limit = self._params.pop('_limit', None)
        stories = Story.get_collection(_limit=_limit)
        Story._update_many(stories, **self._params)

        return JHTTPOk("Updated %s %s(s) objects" % (
            stories.count(), self._model_class.__name__))
