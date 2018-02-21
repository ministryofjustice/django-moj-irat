import os
import sys

from setuptools import setup

root_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_path, 'README.rst')) as readme:
    README = readme.read()

tests_require = ['responses>=0.5']
if sys.version_info < (3, 3):
    tests_require.append('mock>=1.3')

setup(
    name='django-moj-irat',
    version='0.3',
    author='Ministry of Justice Digital Services',
    url='https://github.com/ministryofjustice/django-moj-irat',
    packages=['moj_irat'],
    include_package_data=True,
    license='BSD License',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=['Django>=1.8', 'requests'],
    tests_require=tests_require,
    test_suite='runtests.runtests',
)
