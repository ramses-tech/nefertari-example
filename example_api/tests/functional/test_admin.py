from example_api.model import User
from example_api.tests import TestView


class TestAdmin(TestView):
    def setUp(self):
        self.app  # this bootstraps
        self.tearDown()

        self.user = User(
            username='test_user',
            password='123',
            email='test_user@email.com').save()
        self.system = User(
            username='test_system',
            password='123',
            email='test_system@email.com',
            groups=['admin']).save()

        resp = self.app.post_json(
            '/login',
            dict(login=self.system.username, password='123'))
        resp.headers.pop('content-length', None)  # remove the length

        self.headers = resp.headers

    def _status(self, status):
        return dict(
            headers=self.headers,
            status=status)

    def tearDown(self):
        self.app.post('/logout')
        User.drop_collection()

    # users
    def test_user_index(self):
        self.app.get('/users', **self._status(200))

    def test_user_create(self):
        self.app.post_json(
            '/users',
            dict(
                username='new_user',
                password='123',
                email='new_user@email.com'),
            **self._status(201))

    def test_user_delete(self):
        self.app.delete('/users/test_user', **self._status(200))

    def test_user_show(self):
        self.app.get('/users/test_system', **self._status(200))

        resp = self.app.get('/users/test_user', **self._status(200))
        self.assertTrue('groups' in resp.json_body)
        self.assertTrue('email' in resp.json_body)
        self.assertTrue('settings' in resp.json_body)

    def test_user_update(self):
        self.app.put_json(
            '/users/test_user',
            dict(),
            **self._status(200))

        self.app.put_json(
            '/users/test_user',
            dict(first_name='bobo'),
            **self._status(200))

        self.user.reload()
        assert self.user.first_name == 'bobo'

        self.app.put_json(
            '/users/test_user',
            dict(username='new_test_user'),
            **self._status(200))

        self.user.reload()
        assert self.user.username == 'new_test_user'
