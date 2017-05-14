Release Notes
=============

v1.1.5
------

* Added Kubernetes Support
* Updatd support for docker-compose and ECS
* Properly split lines for cmd and entrypoint in ECS
* Added automated deployment to Pypi
* Bumped docker python to 3.6

v1.1.4
------

* Added Chronos task support
* Fixed ``privileged`` for Marathon output
* Added support for Mesos fetcher

v1.1.3
------

* Switched docker image to python:3.5-alpine (604 MB smaller, 77 MB total)
* Fixed case when compose specifies command as an array

v1.1.2
------

* Fixed udp port handling
* Added support for ``pid`` and ``env-file`` parameters
* Added docs for adding parameters and creating new transformers

v1.1.1
------

* Added environment variable support for command line options
* Added short form for command line options
* CPU is no longer required for ECS

v1.1.0
------

* Added Marathon task support
* Correctly handle compose version type - `GH #46`_
* Assume compose memory is in bytes - `GH #41`_

.. _GH #46: https://github.com/micahhausler/container-transform/pull/46
.. _GH #41: https://github.com/micahhausler/container-transform/pull/41

v1.0.0
------

* Fixed `GH #35`_
* Removed fig support
* Added support for labels
* Added support for docker-compose v2
* Added support for log drivers - `GH #33`_

.. _GH #35: https://github.com/micahhausler/container-transform/issues/35
.. _GH #33: https://github.com/micahhausler/container-transform/issues/33


v0.6.1
------

* Fix ``after`` names in Systemd
* Fixed invalid volume name for ECS volumes
* Added support for exec form of command and entrypoint

v0.6.0
------

* Added Systemd as an output type

v0.5.1
------

* Fixed issue where ECS host port was accidentally assigned when unspecified

v0.5.0
------

Features
~~~~~~~~
* Added support for local volumes
* Output full ECS task json, including volume info

Internal
~~~~~~~~
* converted static methods to class methods to keep track of volume information

v0.4
----

* Added support for `docker compose`_
* docker-compose is now the default input type

.. _docker compose: https://docs.docker.com/compose/

v0.3
----

* Added support for `volumesFrom`_ in ECS Task Definitions

.. _volumesFrom: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_defintions.html#using_data_volumes

v0.2
----

* Redesign of transformer classes
* Added ability to read in ECS tasks and write fig configuration

v0.1
----

* This is the initial release of container-transform.
* Includes a Fig to ECS transformer
