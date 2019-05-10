doconf
======

Configuration specified through documentation.

Installation
------------

From the project root directory::

    $ python setup.py install

Or from pip::

    $ pip install doconf

Usage
-----

Use --help/-h to view info on the arguments::

    $ doconf --help

Find will show you where the config would be loaded from in the current environment::

    $ doconf find examples.my_example_app.config:CustomConfig

Validate will find your config and parse it, tell you whether it has all required variables and show you the values::

    $ doconf validate examples.my_example_app.config:CustomConfig --config-path examples/my_example_app/my_example_app.cfg

Generate will dump example configuration files for you to provide as examples::

    $ doconf generate examples.my_example_app.config:CustomConfig --out .

Release Notes
-------------

:0.0.1:
    Project created
