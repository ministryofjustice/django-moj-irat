import json

from django.template.loaders.app_directories import Loader
from django.test import SimpleTestCase


class DummyTemplateLoader(Loader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        return 'dummy', 'dummy'


class TestCase(SimpleTestCase):
    def assertJsonResponse(self, response, expected_data, status_code=200):
        self.assertEqual(response.status_code, status_code)
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(json_response, expected_data)
