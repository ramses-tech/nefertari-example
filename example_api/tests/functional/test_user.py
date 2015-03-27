import unittest
import json
import cookielib

from example_api.tests import TestView
from example_api.model import *

class TestUser(TestView):
    def setUp(self):
        self.app #this bootstraps
        self.tearDown()

        user = User(username='test_user', password='123', email='test_user@email.com', groups=['user']).save()
        User(username='test_system', password='123', email='test_system@email.com', groups=['admin']).save()

        #other user
        other_user = User(username='test_other_user', password='123', email='test_other_user@email.com').save()

        resp = self.app.post_json('/login',
                    dict(login=user.username, password='123'))

        resp.headers.pop('content-length', None) #remove the length
        self.headers = resp.headers

    def _status(self, status):
        return dict(
            headers=self.headers,
            status=status)

    def tearDown(self):
        self.app.post('/logout')
        User.objects.delete()

    #users
    def test_user_index(self):
        self.app.get('/users', **self._status(403))

    def test_user_create(self):
        self.app.post_json('/users', **self._status(400))

    def test_user_delete(self):
        self.app.delete('/users/test_user', **self._status(403))
        self.app.delete('/users/test_other_user', **self._status(403))

    def test_user_show(self):
        resp = self.app.get('/users/test_system', **self._status(200))

        resp1 = self.app.get('/users/test_user', **self._status(200))
        resp2 = self.app.get('/users/self', **self._status(200))

        self.assertEqual(resp1.json_body, resp2.json_body)

        #other user's info is reduced. does not show groups, email etc.
        resp3 = self.app.get('/users/test_other_user', **self._status(200))
        self.assertFalse('groups' in resp3.json_body)
        self.assertFalse('email' in resp3.json_body)
        self.assertFalse('settings' in resp3.json_body)

    def test_user_update(self):
        response = self.app.put('/users/test_user', **self._status(200))
        response = self.app.put('/users/test_other_user', **self._status(403))
