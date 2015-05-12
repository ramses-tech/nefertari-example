import unittest
import mock
import webtest
import ConfigParser


def bootstrap():
    conf_parser = ConfigParser.SafeConfigParser()
    conf_parser.read('test.ini')
    conf = dict(conf_parser.items('app:example_api'))

    from example_api import main
    return webtest.TestApp(main({}, **conf))


class TestView(unittest.TestCase):
    _app = None

    @property
    def app(self):
        if TestView._app:
            return TestView._app
        TestView._app = bootstrap()
        return TestView._app


class _ESDocs(list):
    pass


patched = [
    mock.patch(
        'nefertari.elasticsearch.ES.get_collection',
        return_value=_ESDocs()),
]


def setUpPackage():
    [p.start() for p in patched]


def tearDownPackage():
    mock.patch.stopall()
