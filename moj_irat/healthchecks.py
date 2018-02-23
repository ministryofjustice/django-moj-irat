import inspect

from django.conf import settings
from django.utils.module_loading import autodiscover_modules, import_string

DEFAULT_HEALTHCHECKS = ['moj_irat.healthchecks.database_healthcheck']


class HealthcheckResponse(object):
    def __init__(self, name, status, **kwargs):
        self.name = name
        self.status = status
        self.kwargs = kwargs

    def __str__(self, *args, **kwargs):
        return '%s: %s' % (self.name, 'Passed' if self.status else 'Failed')

    def get_dict(self):
        data = {
            'name': self.name,
            'status': self.status,
        }
        if self.kwargs:
            data.update(self.kwargs)
        return data


def database_healthcheck():
    """
    Healthcheck for connecting to the default Django database
    """
    from django.db import connection

    connection.cursor()
    return True


database_healthcheck.name = 'database'


def get_key_path(data, path):
    if not path:
        return data
    if isinstance(data, list):
        next_data = data[int(path[0])]
    else:
        next_data = data[path[0]]
    return get_key_path(next_data, path[1:])


class UrlHealthcheck(object):
    """
    Healthcheck for loading a URL
    """

    def __init__(self, name, url, method='get',
                 data=None, headers=None, auth=None,
                 status_code=200, timeout=5, allow_redirects=False,
                 text_in_response=None, value_at_json_path=None):
        """
        :param name: the name of this check
        :param url: url to request
        :param method: HTTP method to use
        :param data: optional data to send
        :param headers: additional headers
        :param auth: optional authentication
        :param status_code: expected response status
        :param timeout: max time to try loading
        :param allow_redirects: whether redirects should be followed
        :param text_in_response: expected text in response
        :param value_at_json_path: expected value at path in json response,
            tuple of (value, dotted path)
        :type value_at_json_path: tuple
        """
        self.name = name
        self.url = url
        self.method = method
        self.data = data
        self.headers = headers
        self.auth = auth
        self.status_code = status_code
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.text_in_response = text_in_response
        self.value_at_json_path = value_at_json_path

    def __call__(self):
        import requests

        try:
            method = getattr(requests, self.method)
            url_response = method(self.url, data=self.data,
                                  headers=self.headers, auth=self.auth,
                                  timeout=self.timeout,
                                  allow_redirects=self.allow_redirects)
            if self.status_code is not None and \
                    url_response.status_code != self.status_code:
                return self.error_response('Response status was not %s' %
                                           self.status_code)
            if self.text_in_response is not None and \
                    self.text_in_response not in url_response.text:
                return self.error_response('Response text did not contain %s' %
                                           self.text_in_response)
            if self.value_at_json_path is not None:
                expected_value = self.value_at_json_path[0]
                json_path = self.value_at_json_path[1]
                try:
                    value = get_key_path(url_response.json(), json_path.split('.'))
                except (KeyError, IndexError, ValueError):
                    return self.error_response('Response JSON path "%s" does not exist' %
                                               json_path)
                if value != expected_value:
                    return self.error_response('Response JSON path "%s" did not contain "%s"' %
                                               (json_path, expected_value))
        except requests.Timeout:
            return self.error_response('Timed out')
        except requests.HTTPError:
            return self.error_response('URL not loaded')

        return self.success_response(url_response)

    def error_response(self, error):
        return HealthcheckResponse(self.name, False, error=error,
                                   url=self.url)

    def success_response(self, url_response):
        return HealthcheckResponse(self.name, True, url=self.url)


class JsonUrlHealthcheck(UrlHealthcheck):
    """
    Healthcheck for loading a JSON URL and including it in the response
    """

    def success_response(self, url_response):
        response = super(
            JsonUrlHealthcheck,
            self
        ).success_response(url_response)
        try:
            response.kwargs['response'] = url_response.json()
        except ValueError:
            response.kwargs['response'] = 'JSON response cannot be parsed'
        return response


class HealthcheckRegistry(object):
    """
    Healthcheck registry - loads and runs healthchecks.  A healthcheck is a
    callable, or a class whose instances are callable, that returns a bool,
    a HealthcheckResponse or raises an exception.
    """

    def __init__(self):
        self._registry = []
        self._registry_loaded = False

    def reset(self):
        self._registry = []
        self._registry_loaded = False

    def load_healthchecks(self):
        """
        Loads healthchecks.
        """
        self.load_default_healthchecks()
        if getattr(settings, 'AUTODISCOVER_HEALTHCHECKS', True):
            self.autodiscover_healthchecks()
        self._registry_loaded = True

    def load_default_healthchecks(self):
        """
        Loads healthchecks specified in settings.HEALTHCHECKS as dotted import
        paths to the classes. Defaults are listed in `DEFAULT_HEALTHCHECKS`.
        """
        default_healthchecks = getattr(settings, 'HEALTHCHECKS', DEFAULT_HEALTHCHECKS)
        for healthcheck in default_healthchecks:
            healthcheck = import_string(healthcheck)
            self.register_healthcheck(healthcheck)

    def autodiscover_healthchecks(self):
        """
        Loads healthchecks.py in all installed apps. Register healthchecks
        in your healthchecks.py by calling `registry.register_healthcheck`
        """
        autodiscover_modules('healthchecks', register_to=self)

    def register_healthcheck(self, healthcheck):
        """
        Register a healthcheck. Call this method from your apps'
        healthchecks.py and use autodiscovery for loading.
        :param healthcheck: callable or callable class
        """
        self._registry.append(healthcheck)

    def run_healthchecks(self):
        """
        Runs all registered healthchecks and returns a list of
        HealthcheckResponse.
        """
        if not self._registry_loaded:
            self.load_healthchecks()

        def get_healthcheck_name(hc):
            if hasattr(hc, 'name'):
                return hc.name
            return hc.__name__

        responses = []
        for healthcheck in self._registry:
            try:
                if inspect.isclass(healthcheck):
                    healthcheck = healthcheck()
                response = healthcheck()
                if isinstance(response, bool):
                    response = HealthcheckResponse(
                        name=get_healthcheck_name(healthcheck),
                        status=response,
                    )
            except Exception as e:
                response = HealthcheckResponse(
                    name=get_healthcheck_name(healthcheck),
                    status=False,
                    exception=str(e),
                    exception_class=e.__class__.__name__,
                )
            responses.append(response)
        return responses


registry = HealthcheckRegistry()
