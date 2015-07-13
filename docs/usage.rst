Usage
=====

::

    $ container-transform -h
    Usage: container-transform [OPTIONS] [INPUT_FILE]

      container-transform is a small utility to transform various docker
      container formats to one another.

      Default input type is compose, default output type is ECS

      Default is to read from STDIN if no INPUT_FILE is provided

    Options:
      --input-type [ecs|compose|fig]
      --output-type [ecs|compose|fig|systemd]
      -v / --no-verbose        Expand/minify json output
      -q                       Silence error messages
      --version                Show the version and exit.
      -h, --help               Show this message and exit.


ECS Format
----------

`Amazon Documentation`_

.. _Amazon Documentation: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_defintions.html

Docker Compose Format
---------------------

`Docker Compose Documentation`_

.. _Docker Compose Documentation: https://docs.docker.com/compose/

Fig Format
----------

`Fig Documentation`_

.. _Fig Documentation: http://www.fig.sh/yml.html


Systemd Service Units
---------------------

`Systemd Unit Configuration`_

.. _Systemd Unit Configuration: http://www.freedesktop.org/software/systemd/man/systemd.service.html