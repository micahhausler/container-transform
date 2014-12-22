Quickstart
==========
Transform is a small utility to transform various docker container formats to one another.

Currently only input type is Fig and output type is EC2 Container Service

Example usage:

.. code-block:: bash

    $ cat fig.yml | container-transform  -v
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
    The output type ECS does not support the parameter 'build'.
    The parameter 'build': '.' will be ignored for container web.

or:

.. code-block:: bash

    $ container-transform  fig.yml -q
    [{"command": ["uwsgi", "--json", "uwsgi.json"], ...
