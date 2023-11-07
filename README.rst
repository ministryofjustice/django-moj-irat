IRaT support for Django
=======================

A set of tools to make it easier to add a Django-based service to Ministry of Justice's Incidence Response and Tuning:

* ping.json view
* healthcheck.json view with extensible healthchecks

Usage
-----

Install using ``pip install django-moj-irat``.

Django settings:

.. code-block:: python

    HEALTHCHECKS = [
        'moj_irat.healthchecks.database_healthcheck',
        # override default list of healthcheck callables
    ]
    AUTODISCOVER_HEALTHCHECKS = True  # whether to autodiscover and load healthcheck.py from all installed apps

Development
-----------

.. image:: https://github.com/ministryofjustice/django-moj-irat/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/ministryofjustice/django-moj-irat/actions/workflows/test.yml

.. image:: https://github.com/ministryofjustice/django-moj-irat/actions/workflows/lint.yml/badge.svg?branch=main
    :target: https://github.com/ministryofjustice/django-moj-irat/actions/workflows/lint.yml

Please report bugs and open pull requests on `GitHub`_.

To work on changes to this library, it’s recommended to install it in editable mode into a virtual environment,
i.e. ``pip install --editable .``

Use ``python -m tests`` to run all tests locally.
Alternatively, you can use ``tox`` if you have multiple python versions.

[Only for GitHub team members] Distribute a new version to `PyPI`_ by:

- updating the ``VERSION`` tuple in ``moj_irat/__init__.py``
- adding a note to the `History`_
- publishing a release on GitHub which triggers an upload to PyPI;
  alternatively, run ``python -m build; twine upload dist/*`` locally

History
-------

Unreleased
    Migrated test, build and release processes away from deprecated setuptools commands.
    No significant library changes.

0.8
    Drop support for python 3.6 and 3.7.
    Add support for python 3.11.
    Add experimental support for Django versions 4.0 & 4.1.
    Improve testing and linting.

0.7
    Add support for python 3.9 and 3.10.
    Improve testing and linting.

0.6
    Drop support for python 3.5.
    Improve linting.

0.5
    Drop python 2 support (now compatible with 3.5 - 3.8).
    Support Django 2.2 - 3.2 (both LTS).

0.4
    Include CORS header.

0.3
    Add python 2 compatibility.

0.2
    Allow including JSON response for healthchecks.

0.1
    Original release.

Copyright
---------

Copyright (C) 2023 HM Government (Ministry of Justice Digital & Technology).
See LICENSE.txt for further details.

.. _GitHub: https://github.com/ministryofjustice/django-moj-irat
.. _PyPI: https://pypi.org/project/django-moj-irat/
