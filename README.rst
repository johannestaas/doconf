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

    usage: doconf [-h] {find,validate,generate} ...

    positional arguments:
      {find,validate,generate}
        find                find where the config file would be loaded from
        validate            validate your config files match the format
        generate            generate example config files

    optional arguments:
      -h, --help            show this help message and exit


Find will show you where the config would be loaded from in the current environment::

    $ doconf find --help
    usage: doconf find [-h] class_path

    positional arguments:
      class_path  path to the module and class, eg:
                  custom_example.config:CustomConfig

    optional arguments:
      -h, --help  show this help message and exit

Here we can see where the environment would discover a config specified by the class CustomConfig in the directory
examples/my_example_app/config.py::

    $ doconf find examples.my_example_app.config:CustomConfig

Validate will find your config and parse it, tell you whether it has all required variables and show you the values::

    $ doconf validate --help | sed 's/        /    /g'
    usage: doconf validate [-h] [--config-path CONFIG_PATH] [--env ENV] class_path

    positional arguments:
      class_path            path to the module and class, eg:
                            custom_example.config:CustomConfig

    optional arguments:
      -h, --help            show this help message and exit
      --config-path CONFIG_PATH, -c CONFIG_PATH
                            direct path to config
      --env ENV, -e ENV     the environment to use

This will validate that the config passed via --config-path matches the format, and we will see the values it sets::

    $ doconf validate examples.my_example_app.config:CustomConfig --config-path examples/my_example_app/my_example_app.cfg

Generate will dump example configuration files for you to provide as examples::

    $ doconf generate --help
    usage: doconf generate [-h] [--out OUT] class_path

    positional arguments:
      class_path         path to the module and class, eg:
                         custom_example.config:CustomConfig

    optional arguments:
      -h, --help         show this help message and exit
      --out OUT, -o OUT  output directory, default to current directory

This will dump out an example documented config for the default environment and the production environment::

    $ doconf generate examples.my_example_app.config:CustomConfig --out .

Release Notes
-------------

:0.1.0:
  - Implemented main logic, including parser and DoconfConfig class.
  - Implemented CLI tools: find, validate, generate.
  - Added examples.
:0.0.1:
  - Project created.
