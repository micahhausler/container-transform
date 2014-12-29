.. image:: https://travis-ci.org/ambitioninc/container-transform.png
   :target: https://travis-ci.org/ambitioninc/container-transform

.. image:: https://coveralls.io/repos/ambitioninc/container-transform/badge.png?branch=develop
    :target: https://coveralls.io/r/ambitioninc/container-transform?branch=develop
.. image:: https://pypip.in/v/container-transform/badge.png
    :target: https://pypi.python.org/pypi/container-transform/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/container-transform/badge.png
    :target: https://pypi.python.org/pypi/container-transform/
    :alt: Number of PyPI downloads


container-transform
===================
Transform is a small utility to transform various docker container formats to one another.

Currently only input type is Fig and output type is EC2 Container Service

Quickstart
----------
::

    $ container-transform  fig.yml -q -v
    [
            {
                "memory": 1024,
                "image": "postgres:9.3",
                "name": "db",
                "essential": true
            },
            {
                "memory": 128,
                "image": "redis:latest",
                "name": "redis",
                "essential": true
            },
            {
                "name": "web",
                "memory": 64,
                "command": [
                    "uwsgi",
                    "--json",
                    "uwsgi.json"
                ],
                "environment": [
                    {
                        "name": "AWS_ACCESS_KEY_ID",
                        "value": "AAAAAAAAAAAAAAAAAAAA"
                    },
                    {
                        "name": "AWS_SECRET_ACCESS_KEY",
                        "value": "1111111111111111111111111111111111111111"
                    }
                ],
                "essential": true
            }
    ]

Installation
------------
To install the latest release, type::

    pip install container-transform

To install the latest code directly from source, type::

    pip install git+git://github.com/ambitioninc/container-transform.git

Documentation
=============

Full documentation is available at http://container-transform.readthedocs.org

License
=======
MIT License (see LICENSE)