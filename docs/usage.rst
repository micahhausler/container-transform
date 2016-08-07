.. _usage:

Usage
=====

::

    $ container-transform -h
    Usage: container-transform [OPTIONS] [INPUT_FILE]

      container-transform is a small utility to transform various docker
      container formats to one another.

      Default input type is compose, default output type is ECS

      Default is to read from STDIN if no INPUT_FILE is provided

      All options may be set by environment variables with the prefix "CT_"
      followed by the full argument name.

    Options:
      -i, --input-type [ecs|compose|marathon|chronos|kubernetes]
      -o, --output-type [ecs|compose|systemd|marathon|chronos|kubernetes]
      -v, --verbose / --no-verbose    Expand/minify json output
      -q, --quiet                     Silence error messages
      --version                       Show the version and exit.
      -h, --help                      Show this message and exit.


Kubernetes Format
-----------------

When consuming Kubernetes input, container-transform supports the following object types:

* ReplicaSet
* Deployment
* DaemonSet
* Pod
* ReplicationController

and will only load the first of those objects in the file.

`Kubernetes Pods`_ & `Kubernetes API Objects`_

.. _Kubernetes Pods: http://kubernetes.io/docs/user-guide/pods/
.. _Kubernetes API Objects: http://kubernetes.io/docs/api-reference/v1/definitions/

ECS Format
----------

`Amazon Documentation`_

.. _Amazon Documentation: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_defintions.html

Docker Compose Format
---------------------

`Docker Compose Documentation`_

.. _Docker Compose Documentation: https://docs.docker.com/compose/

Systemd Service Units
---------------------

`Systemd Unit Configuration`_

.. _Systemd Unit Configuration: http://www.freedesktop.org/software/systemd/man/systemd.service.html

Marathon Applications
---------------------

When consuming Marathon input, container-transform supports:

* A single Marathon application
* Content from the Marathon Group API
* A JSON array of Marathon application objects

When emitting Marathon output, container-transform will emit a list of
applications if there is more than one. Otherwise, it will emit a single
application.

`Marathon Application Basics`_  & `Marathon API docs`_

.. _Marathon Application Basics: http://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon API docs: http://mesosphere.github.io/marathon/docs/generated/api.html

Chronos Tasks
-------------

Chronos tasks are meant to be run as headless tasks and while most docker
options may be passed as parameters, they may not work as intended on a Mesos
cluster.

When consuming Chronos input, container-transform supports:

* A single Chronos task
* A JSON array of Chronos tasks

When emitting Chronos output, container-transform will emit a list of tasks if
there is more than one. Otherwise, it will emit a single task.

.. note::

    A JSON array of tasks is not valid for submitting to the Chronos API, but
    is meant to be a convenience so that the output can be manipulated with
    other tools.


`Chronos API Documentation`_  & `Chronos Job Serializer source code`_

.. _Chronos API Documentation: http://mesos.github.io/chronos/docs/api.html#adding-a-docker-job
.. _Chronos Job Serializer source code: https://github.com/mesos/chronos/blob/master/src/main/scala/org/apache/mesos/chronos/utils/JobSerializer.scala
