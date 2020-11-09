import json
from unittest import mock

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.urls import reverse

from moj_irat.views import PingJsonView
from tests.utils import TestCase


class PingJsonViewTestCase(TestCase):
    def call_ping_json_view(self, **view_kwargs):
        view = PingJsonView.as_view(**view_kwargs)
        request = HttpRequest()
        request.method = 'GET'
        response = view(request)
        return response, json.loads(response.content.decode('utf-8'))

    def test_ping_json_returns_minimum_environment(self):
        env = {
            'DOCKER_IMAGE_DATE': '2015-12-04T10:00:00+0000',
            'DOCKER_IMAGE_SHA': 'e9866935d3c5d19adc48e0be3ad3f2718b86bfe4',
        }
        with mock.patch.dict('os.environ', env):
            response, response_json = self.call_ping_json_view(
                build_date_key='DOCKER_IMAGE_DATE',
                commit_id_key='DOCKER_IMAGE_SHA',
            )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response_json, {
            'build_date': '2015-12-04T10:00:00+0000',
            'commit_id': 'e9866935d3c5d19adc48e0be3ad3f2718b86bfe4',
        })

    def test_ping_json_returns_complete_environment(self):
        env = {
            'APP_BUILD_DATE': '2015-12-04T10:00:00+0000',
            'APP_GIT_COMMIT': 'e9866935d3c5d19adc48e0be3ad3f2718b86bfe4',
            'APP_BUILD_TAG': 'master.latest',
            'JENKINS_TAG': 'TEST Django Utils',
        }
        with mock.patch.dict('os.environ', env):
            response, response_json = self.call_ping_json_view(
                build_date_key='APP_BUILD_DATE',
                commit_id_key='APP_GIT_COMMIT',
                version_number_key='APP_BUILD_TAG',
                build_tag_key='JENKINS_TAG',
            )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response_json, {
            'build_date': '2015-12-04T10:00:00+0000',
            'commit_id': 'e9866935d3c5d19adc48e0be3ad3f2718b86bfe4',
            'version_number': 'master.latest',
            'build_tag': 'TEST Django Utils',
        })

    def test_ping_json_returns_incomplete_environment_as_server_error(self):
        env = {
            'DOCKER_IMAGE_DATE': '2015-12-04T10:00:00+0000',
        }
        with mock.patch.dict('os.environ', env):
            response, response_json = self.call_ping_json_view(
                build_date_key='DOCKER_IMAGE_DATE',
                commit_id_key='DOCKER_IMAGE_SHA',
            )
        self.assertEqual(response.status_code, 501)
        self.assertDictEqual(response_json, {
            'build_date': '2015-12-04T10:00:00+0000',
            'commit_id': None,
        })

    def test_unconfigured_ping_json_environment_fails(self):
        with self.assertRaises(ImproperlyConfigured):
            self.call_ping_json_view(commit_id_key='DOCKER_IMAGE_SHA')

    def test_incomplete_environment_ping_json_view(self):
        response = self.client.get(reverse('ping_json'))
        self.assertJsonResponse(response, {
            'build_date': None,
            'commit_id': None,
            'version_number': None,
            'build_tag': None,
        }, status_code=501)

    def test_complete_environment_ping_json_view(self):
        env = {
            'APP_BUILD_DATE': '2015-12-04T10:00:00+0000',
            'APP_GIT_COMMIT': 'e9866935d3c5d19adc48e0be3ad3f2718b86bfe4',
            'APP_BUILD_TAG': 'master.latest',
            'JENKINS_TAG': 'TEST Django Utils',
        }
        with mock.patch.dict('os.environ', env):
            response = self.client.get(reverse('ping_json'))
        self.assertJsonResponse(response, {
            'build_date': '2015-12-04T10:00:00+0000',
            'commit_id': 'e9866935d3c5d19adc48e0be3ad3f2718b86bfe4',
            'version_number': 'master.latest',
            'build_tag': 'TEST Django Utils',
        })

    def test_cors_header_is_set_correctly(self):
        env = {
            'DOCKER_IMAGE_DATE': '2015-12-04T10:00:00+0000',
            'DOCKER_IMAGE_SHA': 'e9866935d3c5d19adc48e0be3ad3f2718b86bfe4',
        }
        with mock.patch.dict('os.environ', env):
            response, response_json = self.call_ping_json_view(
                build_date_key='DOCKER_IMAGE_DATE',
                commit_id_key='DOCKER_IMAGE_SHA',
            )
        self.assertEqual('*', response['access-control-allow-origin'])
