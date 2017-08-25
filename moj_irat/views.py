import os

from django.core.exceptions import ImproperlyConfigured
from django.http.response import JsonResponse
from django.views.generic import View


class PingJsonView(View):
    """
    View for returning IRaT information from environment variables
    c.f. https://github.com/ministryofjustice/incident-response-schemas/blob/master/ping-dot-json-schema.json

    Usage:
        urlpatterns = [
            ...
            url(r'^ping.json$', PingJsonView.as_view(**environment_key_names), name='ping_json'),
            ...
        ]
    """
    build_date_key = None      # Docker container build date
    commit_id_key = None       # Git SHA from which the image was built
    version_number_key = None  # Docker container tag
    build_tag_key = None       # Jenkins job name and id

    def __init__(self, **kwargs):
        if not kwargs.get('build_date_key') or not kwargs.get('commit_id_key'):
            raise ImproperlyConfigured('ping.json schema requires build_date_key and '
                                       'commit_id_key to be provided')
        super(PingJsonView, self).__init__(**kwargs)

    def get(self, request):
        response_data = {
            attr[:-4]: os.environ.get(getattr(self, attr))
            for attr in dir(self)
            if attr.endswith('_key') and getattr(self, attr)
        }
        response = JsonResponse(response_data)
        if not response_data['build_date'] or not response_data['commit_id']:
            response.status_code = 501

        response['Access-Control-Allow-Origin'] = '*'

        return response


class HealthcheckView(View):
    """
    View for returning the health status of dependency services for IRaT support
    """
    def get(self, request):
        from moj_irat.healthchecks import registry

        response_data = {}
        for response in registry.run_healthchecks():
            response = response.get_dict()
            check_name = response.pop('name')
            response_data[check_name] = response
        all_passed = all(response['status'] for response in response_data.values())
        response_data['*'] = dict(status=all_passed)

        response = JsonResponse(response_data)
        if not all_passed:
            response.status_code = 500
        return response
