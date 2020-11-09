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

.. image:: https://travis-ci.org/ministryofjustice/django-moj-irat.svg?branch=master
    :target: https://travis-ci.org/ministryofjustice/django-moj-irat

Please report bugs and open pull requests on `GitHub`_.

Use ``python setup.py test`` to run all tests.

Distribute a new version by updating the ``version`` argument in ``setup.py:setup`` and
publishing a release in GitHub (this triggers a GitHub Actions workflow to automatically upload it).
Alternatively, run ``python setup.py sdist bdist_wheel upload`` locally.

Copyright
---------

Copyright (C) 2020 HM Government (Ministry of Justice Digital Services).
See LICENSE.txt for further details.

.. _GitHub: https://github.com/ministryofjustice/django-moj-irat
