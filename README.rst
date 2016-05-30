.. image:: https://travis-ci.org/micahhausler/container-transform.png
   :target: https://travis-ci.org/micahhausler/container-transform

.. image:: https://coveralls.io/repos/micahhausler/container-transform/badge.png?branch=master
    :target: https://coveralls.io/r/micahhausler/container-transform?branch=master

.. image:: https://readthedocs.org/projects/container-transform/badge/?version=latest
    :target: http://container-transform.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status


container-transform
===================
container-transform is a small utility to transform various docker container
formats to one another.

Currently, container-transform can parse and convert:

* ECS task definitions
* Docker-compose configuration files
* Marathon Application Definitions or Groups of Applications

and it can output to:

* Systemd unit files


Quickstart
----------
::

    $ cat docker-compose.yml | container-transform  -v
    {
        "family": "python-app",
        "volumes": [
            {
                "name": "host_logs",
                "host": {
                    "sourcePath": "/var/log/myapp"
                }
            }
        ],
        "containerDefinitions": [
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
                "mountPoints": [
                    {
                        "sourceVolume": "host_logs",
                        "containerPath": "/var/log/uwsgi/"
                    }
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
    }
    Container web is missing required parameter "image".
    Container web is missing required parameter "cpu".

Quick Help
----------
::

    Usage: container-transform [OPTIONS] [INPUT_FILE]

      container-transform is a small utility to transform various docker
      container formats to one another.

      Default input type is compose, default output type is ECS

      Default is to read from STDIN if no INPUT_FILE is provided

      All options may be set by environment variables with the prefix "CT_"
      followed by the full argument name.

    Options:
      -i, --input-type [ecs|compose|marathon]
      -o, --output-type [ecs|compose|systemd|marathon]
      -v, --verbose / --no-verbose    Expand/minify json output
      -q, --quiet                     Silence error messages
      --version                       Show the version and exit.
      -h, --help                      Show this message and exit.


Docker Image
------------

To get the docker image, run::

    docker pull micahhausler/container-transform:latest

To run the docker image::

    docker run --rm -v $(pwd):/data/ micahhausler/container-transform  docker-compose.yml

    # or
    cat docker-compose.yml | docker run --rm -i micahhausler/container-transform


Installation
------------

To install the latest release (Python 3 only), type::

    pip install container-transform

To install the latest code directly from source, type::

    pip install git+git://github.com/micahhausler/container-transform.git

Documentation
-------------

Full documentation is available at http://container-transform.readthedocs.org

License
-------
MIT License (see LICENSE)
