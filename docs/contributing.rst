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
    python setup.py install
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
Please contact `hausler.m@gmail.com`_ with the GPG key provided on `keybase`.


.. _hausler.m@gmail.com: mailto:hausler.m@gmail.com
.. _keybase : https://keybase.io/micahhausler
