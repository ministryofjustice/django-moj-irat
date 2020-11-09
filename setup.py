import os

from setuptools import setup

root_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_path, 'README.rst')) as readme:
    README = readme.read()

install_requires = ['requests']
tests_require = ['flake8', 'responses']
django_version = '>=1.10,<2'
install_requires.append('Django%s' % django_version)

setup(
    name='django-moj-irat',
    version='0.4',
    author='Ministry of Justice Digital Services',
    author_email='dev@digital.justice.gov.uk',
    url='https://github.com/ministryofjustice/django-moj-irat',
    packages=['moj_irat'],
    include_package_data=True,
    license='MIT',
    description="Tools to support adding a Django-based service to "
                "Ministry of Justice's Incidence Response and Tuning",
    long_description=README,
    keywords='moj django irat monitoring',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='tests.run',
)
