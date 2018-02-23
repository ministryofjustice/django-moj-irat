import json

from django.test import SimpleTestCase


class TestCase(SimpleTestCase):
    def assertJsonResponse(self, response, expected_data, status_code=200):  # noqa
        self.assertEqual(response.status_code, status_code)
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(json_response, expected_data)
