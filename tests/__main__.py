import pathlib
import sys

if __name__ == '__main__':
    import django
    from django.conf import settings
    from django.test.runner import DiscoverRunner

    tests_path = pathlib.Path(__file__).parent
    root_path = tests_path.parent

    test_settings = dict(
        DEBUG=True,
        SECRET_KEY='a' * 24,
        ROOT_URLCONF='tests.urls',
        INSTALLED_APPS=(
            'moj_irat',
        ),
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
        }],
    )

    if not settings.configured:
        settings.configure(**test_settings)
        django.setup()

    test_runner = DiscoverRunner(verbosity=2, failfast=False, interactive=False)
    failures = test_runner.run_tests(['tests'])
    sys.exit(failures)
