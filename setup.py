# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
import re
from setuptools import setup, find_packages
assert multiprocessing


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'container_transform/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))

install_requires = [
    'PyYAML>=3.10,<4',
    'six>=1.3.0,<2',
    'enum34>=1.0.4',
    'click>=3.3',
]
tests_require = [
    'coverage>=3.7.1',
    'flake8>=2.2.0',
    'mock>=1.0.1',
    'nose>=1.3.0',
]

extras_require = {
    'test': tests_require,
    'packaging': ['wheel'],
    'docs': ['Sphinx>=1.2.2', 'sphinx_rtd_theme'],
}

everything = set(install_requires)
for deps in extras_require.values():
    everything.update(deps)
extras_require['all'] = list(everything)


setup(
    name='container-transform',
    version=get_version(),
    description='A converter for various docker cluster formats',
    long_description=open('README.rst').read(),
    url='https://github.com/ambitioninc/container-transform',
    author='Micah  Hausler',
    author_email='opensource@ambition.com',
    keywords='docker, container, fig, ecs, compose',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points='''
        [console_scripts]
        container-transform=container_transform.client:transform
    ''',
    license='MIT',
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=tests_require,
    extras_require=extras_require,
    zip_safe=False,
)
