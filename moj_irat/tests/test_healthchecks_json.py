import gc
import re
import sys
try:
    from unittest import mock
except ImportError:
    import mock

from django.core.urlresolvers import reverse
from django.test.utils import override_settings
import responses

from moj_irat.tests.utils import TestCase
from moj_irat.healthchecks import registry


class HealthcheckTestCase(TestCase):
    re_test_app_modules = re.compile(r'^moj_irat\.tests.app(\.|$)')

    def setUp(self):
        registry.reset()
        self.unload_test_app()

    def unload_test_app(self):
        # may not necessarily work in non-cpython
        modules_to_delete = [
            module
            for module in sys.modules
            if self.re_test_app_modules.match(module)
        ]
        for module in modules_to_delete:
            del sys.modules[module]
        gc.collect()

    @override_settings(AUTODISCOVER_HEALTHCHECKS=False)
    def test_load_default_healthchecks(self):
        registry.load_healthchecks()

        expected_names = ['database_healthcheck']
        healthcheck_names = [healthcheck.__name__ for healthcheck in registry._registry]
        self.assertListEqual(healthcheck_names, expected_names)

    @override_settings(INSTALLED_APPS=['moj_irat', 'moj_irat.tests.app'],
                       HEALTHCHECKS=[])
    def test_healthchecks_autodiscovery(self):
        registry.load_healthchecks()
        expected_names = ['PassingResponseHealthcheck', 'PassingExtraResponseHealthcheck',
                          'passing_bool_healthcheck', 'failing_bool_healthcheck',
                          'error_healthcheck']
        healthcheck_names = [healthcheck.__name__ for healthcheck in registry._registry]
        self.assertListEqual(healthcheck_names, expected_names)

    @mock.patch('moj_irat.healthchecks.database_healthcheck')
    def test_default_healthcheck_view(self, mocked_database_healthcheck):
        mocked_database_healthcheck.return_value = True
        mocked_database_healthcheck.name = 'database'

        response = self.client.get(reverse('healthcheck_json'))
        self.assertJsonResponse(response, {
            'database': {
                'status': True
            },
            '*': {
                'status': True
            }
        })

    @override_settings(INSTALLED_APPS=['moj_irat', 'moj_irat.tests.app'],
                       HEALTHCHECKS=[])
    def test_healthcheck_view_with_responses(self):
        response = self.client.get(reverse('healthcheck_json'))

        # must be after view call to not inadvertently cause registration
        from moj_irat.tests.app.healthchecks import passing_bool_healthcheck, \
            failing_bool_healthcheck, error_healthcheck

        healthchecks = [passing_bool_healthcheck, failing_bool_healthcheck, error_healthcheck]

        for func in healthchecks:
            self.assertListEqual(func.get_calls(), [
                {
                    'args': (),
                    'kwargs': {},
                }
            ])

        self.assertJsonResponse(response, {
            'passing_bool_healthcheck': {
                'status': True
            },
            'failing_bool': {
                'status': False
            },
            'error_healthcheck': {
                'status': False,
                'exception': 'error',
                'exception_class': 'ValueError',
            },
            'class': {
                'status': True,
            },
            'class_extra': {
                'status': True,
                'extra': 'extra message',
            },
            '*': {
                'status': False
            }
        }, status_code=500)

    @responses.activate
    def test_url_healthcheck(self):
        from moj_irat.healthchecks import UrlHealthcheck

        url = 'http://www.example.com/'
        value_at_json_path = (123, 'results.0.test')
        healthcheck = UrlHealthcheck(name='url', url=url, status_code=201,
                                     value_at_json_path=value_at_json_path)

        responses.add(responses.GET, url, json={
            'results': [
                {
                    'test': 123
                }
            ]
        }, status=201)
        response = healthcheck()

        self.assertTrue(response.status)
        self.assertEqual(response.name, 'url')
        self.assertEqual(response.kwargs['url'], url)

    @responses.activate
    def test_json_url_healthcheck(self):
        from moj_irat.healthchecks import JsonUrlHealthcheck

        url = 'http://www.example.com/'
        value_at_json_path = (123, 'results.0.test')
        healthcheck = JsonUrlHealthcheck(name='url', url=url, status_code=201,
                                         value_at_json_path=value_at_json_path)

        json_response = {
            'results': [
                {
                    'test': 123
                }
            ]
        }
        responses.add(responses.GET, url, json=json_response, status=201)
        response = healthcheck()

        self.assertTrue(response.status)
        self.assertEqual(response.name, 'url')
        self.assertEqual(response.kwargs['url'], url)
        self.assertEqual(response.kwargs['response'], json_response)
