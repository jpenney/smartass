========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/smartass/badge/?style=flat
    :target: https://smartass.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/jpenney/smartass.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/jpenney/smartass

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/jpenney/smartass?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/jpenney/smartass

.. |requires| image:: https://requires.io/github/jpenney/smartass/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/jpenney/smartass/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/jpenney/smartass/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/jpenney/smartass

.. |version| image:: https://img.shields.io/pypi/v/smartass.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/smartass

.. |wheel| image:: https://img.shields.io/pypi/wheel/smartass.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/smartass

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/smartass.svg
    :alt: Supported versions
    :target: https://pypi.org/project/smartass

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/smartass.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/smartass

.. |commits-since| image:: https://img.shields.io/github/commits-since/jpenney/smartass/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jpenney/smartass/compare/v0.1.0...master



.. end-badges

Apply smart punctuation to subtitles.

* Free software: BSD 3-Clause License

Installation
============

::

    pip install smartass

You can also install the in-development version with::

    pip install https://github.com/jpenney/smartass/archive/master.zip


Documentation
=============


https://smartass.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox