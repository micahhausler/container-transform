Quickstart
==========
container-transform is a small utility to transform various docker container
formats to one another.

Currently, container-transform can parse and convert ECS task definitions and
fig configuration files. Any missing required parameters are printed to STDOUT.

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
    Container db is missing required parameter "cpu".
    Container redis is missing required parameter "cpu".
    Container web is missing required parameter "image".
    Container web is missing required parameter "cpu".

or:

.. code-block:: bash

    $ container-transform  --input-type ecs --output-type fig task.json
    db:
      image: postgres:9.3
      mem_limit: 1073741824b
    redis:
      image: redis:latest
      mem_limit: 134217728b
    web:
      command: uwsgi --json uwsgi.json
      environment:
        AWS_ACCESS_KEY_ID: AAAAAAAAAAAAAAAAAAAA
        AWS_SECRET_ACCESS_KEY: '1111111111111111111111111111111111111111'
      mem_limit: 67108864b

    Container web is missing required parameter "image".

