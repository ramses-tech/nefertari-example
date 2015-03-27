from example_api.tests import TestView
from example_api.model import *

class TestGuest(TestView):
    def setUp(self):
        self.app #this bootstraps
        self.tearDown()

        self.user = User(username='test_user', password='123', email='test_user@email.com').save()

    def tearDown(self):
        self.app.post('/logout')

        User.objects.delete()

    #users
    def test_user_index(self):
        self.app.get('/users', status=403)

    def test_user_create(self):
        self.app.post('/users', status=400)

    def test_user_delete(self):
        self.app.delete('/users/test_user', status=403)

    def test_user_show(self):
        resp = self.app.get('/users/test_user', status=200)
        # self.assertEqual(resp.json_body, {})

    def test_user_update(self):
        response = self.app.put('/users/test_user', status=403)
