from functools import wraps

from moj_irat.healthchecks import HealthcheckResponse, registry


def _track_calls(func):
    @wraps(func)
    def inner(*args, **kwargs):
        func.calls.append({
            'args': args,
            'kwargs': kwargs,
        })
        return func(*args, **kwargs)

    func.calls = []
    inner.get_calls = lambda: func.calls
    return inner


class PassingResponseHealthcheck:
    def __call__(self, *args, **kwargs):
        return HealthcheckResponse('class', True)


class PassingExtraResponseHealthcheck:
    def __call__(self, *args, **kwargs):
        return HealthcheckResponse('class_extra', True, extra='extra message')


@_track_calls
def error_healthcheck():
    raise ValueError('error')


@_track_calls
def passing_bool_healthcheck():
    return True


@_track_calls
def failing_bool_healthcheck():
    return False


failing_bool_healthcheck.name = 'failing_bool'

registry.register_healthcheck(PassingResponseHealthcheck)
registry.register_healthcheck(PassingExtraResponseHealthcheck)
registry.register_healthcheck(passing_bool_healthcheck)
registry.register_healthcheck(failing_bool_healthcheck)
registry.register_healthcheck(error_healthcheck)
