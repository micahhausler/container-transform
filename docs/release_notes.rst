Release Notes
=============

v0.5.0a2
--------

Features
~~~~~~~~
* Added support for local volumes

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
