Contributing
============

Contributions and issues are most welcome! All issues and pull requests are
handled through github on the `issues page`_. Also, please check for
any existing issues before filing a new one. If you have a great idea but it
involves big changes, please file a ticket before making a pull request! We
want to make sure you don't spend your time coding something that might not fit
the scope of the project.

.. _issues page: https://github.com/micahhausler/container-transform/issues

Running the tests
-----------------

To get the source source code and run the unit tests, run::

    git clone git://github.com/micahhausler/container-transform.git
    cd container-transform
    virtualenv env
    . env/bin/activate
    pip install -e .[all]
    python setup.py nosetests

While 100% code coverage does not make a library bug-free, it significantly
reduces the number of easily caught bugs! Please make sure coverage is at 100%
before submitting a pull request!

Code Quality
------------

For code quality, please run flake8::

    $ pip install flake8
    $ flake8 .

Code Styling
------------
Please arrange imports with the following style

.. code-block:: python

    # Standard library imports
    import os

    # Third party package imports
    from mock import patch

    # Local package imports
    from container_transform.version import __version__

Please follow `Google's python style`_ guide wherever possible.

.. _Google's python style: http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

Building the docs
-----------------

When in the project directory::

    pip install -e .[all]
    python setup.py build_sphinx
    open docs/_build/html/index.html

Adding a new parameter
----------------------

If there is a docker parameter that you'd like to add support for, here's a
quick overview of what is involved:

1. Make a new parameter in the ``ARG_MAP`` in the file ``container-transform/schema.py``
2. Check what the parameter name is for each supported transformation type.
   There are links to the documentation for each type on the :doc:`usage` page
3. Create an ``ingest_<param>`` and ``emit_<param>`` method on the
   :class:`BaseTransformer<container_transform.transformer.BaseTransformer>` class
4. Add any data transformations by overriding the base methods that each format
   requires.
5. Add tests to cover any new logic. Don't just use a client test to make
   coverage 100%

Adding a new Transformer
------------------------

If you'd like to add a new format, please create an issue before making a pull
request in order to discuss any major design decisions before putting in
valuable time writing the actual code.

Below is a rough checklist of creating a new transformer type:

* Create a file and class in the base :py:mod:`container_transform` module
* Implement all abstract methods on the :class:`BaseTransformer<container_transform.transformer.BaseTransformer>`
  class
* Add the class to the ``TRANSFORMER_CLASSES`` in the ``converter.py`` file.
* Add the type to the enums at the top of the ``schema.py`` file.
* Add a key to each of the dictionaries in the ``ARG_MAP`` parameters
* If a docker parameter is not supported in your transformer, still create
  a dictionary for it, but set the name to ``None``
* Create a test file in the tests module for your transformer. Try to get at
  least 90% coverage of your transformer before adding any tests to the
  :py:mod:`client_tests.py<container_transform.tests.client_test>` module.
* Add client tests just to make sure the command doesn't blow up
* Add documentation and API links on the :doc:`usage` page.
* Update the usage text output on the ``README.rst`` and the :doc:`usage` page
* Add the type to the format list on the :doc:`index` and ``README.rst`` 

Possible Transformer implementations:

* `Elastic Beanstalk (based on ECS)`_
* `Kubernetes`_ pod
* `Nomad`_ job specification

.. _Elastic Beanstalk (based on ECS): http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker_v2config.html#create_deploy_docker_v2config_dockerrun_format
.. _Kubernetes: http://kubernetes.io/docs/user-guide/pods/multi-container/#pod-configuration-file
.. _Nomad: https://www.nomadproject.io/docs/jobspec/json.html


Release Checklist
-----------------

Before a new release, please go through the following checklist:

* Bump version in container_transform/version.py
* Add a release note in docs/release_notes.rst
* Git tag the version
* Upload to pypi::

    pip install -e .[packaging]
    python setup.py sdist bdist_wheel upload

* Increment the version to ``x.x-dev``

Vulnerability Reporting
-----------------------

For any security issues, please do NOT file an issue or pull request on github!
Please contact `hausler.m@gmail.com`_ with the GPG key provided on `keybase`_.


.. _hausler.m@gmail.com: mailto:hausler.m@gmail.com
.. _keybase: https://keybase.io/micahhausler
