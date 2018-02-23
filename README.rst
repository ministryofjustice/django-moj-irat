IRaT support for Django
=======================

A set of tools to make it easier to add a Django-based service to Ministry of Justice's Incidence Response and Tuning:

* ping.json view
* healthcheck.json view with extensible healthchecks

healthcheck.json
----------------

Django settings:

.. code-block:: python

    HEALTHCHECKS = [
        'moj_irat.healthchecks.database_healthcheck',
        # override default list of healthcheck callables
    ]
    AUTODISCOVER_HEALTHCHECKS = True  # whether to autodiscover and load healthcheck.py from all installed apps

Installation
------------

.. image:: https://travis-ci.org/ministryofjustice/django-moj-irat.svg?branch=master
    :target: https://travis-ci.org/ministryofjustice/django-moj-irat

At the moment, the only way to install the library is from github

.. code-block:: bash

    pip install git+https://github.com/ministryofjustice/django-moj-irat.git

Copyright
---------

Copyright (C) 2018 HM Government (Ministry of Justice Digital Services).
See LICENSE.txt for further details.
