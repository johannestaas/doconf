doconf
======

Configuration specified through documentation.

Installation
------------

From the project root directory::

    $ python setup.py install

Or from pip::

    $ pip install doconf

API Usage
---------

doconf is relatively simple to use. Simply install it, then write out a config module with
a class in a similar format::

    from doconf import DoconfConfig


    class Config(DoconfConfig):
        '''
        name: echo_server

        {default}

        [server]
        HOST (str:"127.0.0.1"): this is the host passed to the app, by default serves locally
        PORT (int:8080): by default it serves on port 8080.
        DEBUG (bool:true): Debug mode is on by default

        [logger]
        LOG_LEVEL (str): the log level, one of debug/info/warning/error. This is required since it has no default
        LOG_PATH: we didn't specify a type so it is by default a string, and required.
        LOG_FORMAT (str:null): None by default

        {production}
        HOST (str:"0.0.0.0"): serve to the world
        PORT (int:8081): serve on port 8081
        DEBUG (bool:false): default to false for production

        [logger]
        LOG_LEVEL (str:"INFO"): default to INFO in production
        LOG_PATH (str:"/var/log/echo_server.log"): put in /var/log/ in production
        LOG_FORMAT (str:null): don't care still
        '''
        pass


    config = Config.load()


In the above example, we can see that we specified a subclass of DoconfConfig, and it's a config for
an app named "echo_server".
We specify a {default} environment first (required), and a few sections and variables with their types and
default values.
Then we specify a {production} environment next and make a few changes to defaults.

Using that, we can now load our config wth ``Config.load()`` below the class definition. It'll automatically
look for echo_server.{conf,cfg,config} in serveral locations depending on the environment, and validate the
config it finds and load it and coerce the values into the types specified. It'll raise an error if a required
value (missing default value) isn't defined, or if the type is wrong.


CLI Usage
---------

You can use the CLI tools to find where it locates its config (``doconf find <classpath>``), you can generate
example documented configs using ``doconf generate <classpath>``, and you can validate configuration files
with ``doconf validate <classpath>``.

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
