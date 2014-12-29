Usage
=====

::

    $ container-transform -h
    Usage: container-transform [OPTIONS] [INPUT_FILE]

      container-transform is a small utility to transform various docker
      container formats to one another.

      Default input type is fig, default output type is ECS

      Default is to read from STDIN if no INPUT_FILE is provided

    Options:
      --input-type [ecs|fig]
      --output-type [ecs|fig]
      -v / --no-verbose        Expand/minify json output
      -q                       Silence error messages
      --version                Show the version and exit.
      -h, --help               Show this message and exit.


ECS Format
----------

`Amazon Documentation`_

.. _Amazon Documentation: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_defintions.html

Fig Format
----------

`Fig Documentation`_

.. _Fig Documentation: http://www.fig.sh/yml.html
