'''
doconf.config
-------------

Core doconf logic lies here.
'''
import os
from configparser import ConfigParser

from .exceptions import (
    DoconfClassError, DoconfFileError, DoconfTypeError, DoconfBadConfigError,
    DoconfUndefinedEnvironmentError,
)
from .parser import parse_docs, parse_as


class MetaConfig(type):
    def __new__(cls, name, bases, dct):
        if name == 'DoconfConfig':
            return super(MetaConfig, cls).__new__(cls, name, bases, dct)
        docs = dct['__doc__']
        if docs is None:
            raise DoconfClassError(
                'class {!r} has no config template documented.'.format(
                    name,
                )
            )
        parse_docs(docs.splitlines(), dct)
        return super(MetaConfig, cls).__new__(cls, name, bases, dct)


class DoconfSection(dict):

    def __getitem__(self, item):
        return super().__getitem__(item.upper())

    def get(self, item, **kwargs):
        return super().get(item.upper(), **kwargs)

    def __contains__(self, item):
        return super().__contains__(item.upper())


class DoconfConfig(metaclass=MetaConfig):

    @classmethod
    def load(cls, path=None, text=None, env='DEFAULT'):
        config = ConfigParser()
        if text is not None:
            config.read_string(text)
        else:
            if path and not os.path.isfile(path):
                raise DoconfFileError('No config file at {!r}'.format(path))
            if not path:
                discoverable = cls.possible_paths()
                for path in discoverable:
                    if os.path.isfile(path):
                        break
                else:
                    raise DoconfFileError(
                        'no config path discovered for {!r}, checked:\n - {}'
                        .format(cls._NAME, '\n - '.join(discoverable))
                    )
            config.read(path)
        return cls(config=config, env=env)

    @classmethod
    def possible_paths(cls):
        '''
        Discover possible configuration paths.
        Need to check if $XDG_CONFIG_HOME exists (default ~/.config/), or if
        $XDG_CONFIG_DIRS exists, and split on :
        '''
        filenames = [
            x.format(cls._NAME)
            for x in ['{}.cfg', '{}.config', '{}.conf']
        ]
        dirs = ['.']
        if os.getenv('HOME'):
            dirs.append(os.getenv('HOME'))
            dirs.append(os.path.expanduser('~/.config'))
            dirs.append(os.path.expanduser('~/.config/{}'.format(cls._NAME)))
        if os.getenv('XDG_CONFIG_HOME'):
            dirs.append(os.getenv('XDG_CONFIG_HOME'))
            dirs.append(os.path.join(
                os.getenv('XDG_CONFIG_HOME'),
                cls._NAME,
            ))
        if os.getenv('XDG_CONFIG_DIRS'):
            for d in os.getenv('XDG_CONFIG_DIRS').split(':'):
                dirs.append(d)
                dirs.append(os.path.join(d, cls._NAME))
        dirs.append('/etc/{}'.format(cls._NAME))
        dirs.append('/etc')

        discoverable = []
        for d in dirs:
            for f in filenames:
                path = os.path.join(d, f)
                discoverable.append(path)
        return discoverable

    def __init__(self, config=None, env='DEFAULT'):
        self._config = config
        if env.lower() not in self.__class__._ENVS:
            raise DoconfUndefinedEnvironmentError(
                'missing environment {!r}'.format(env)
            )
        self._default = self.__class__._ENVS[env.lower()]
        self._values = {}
        self.parse()

    def parse(self):
        self._parsed = {}
        for d_sect in self._default.sections:
            sect_values = DoconfSection()
            self._values[d_sect.name] = sect_values
            self._values[d_sect.name].update(d_sect.defaults)
            try:
                sect = self._config[d_sect.name]
            except KeyError:
                if d_sect.has_required:
                    raise DoconfBadConfigError(
                        'missing section {!r} and it has required variables'
                        .format(d_sect.name)
                    )
                else:
                    # Missing section, but it doesn't have any required
                    # variables.
                    continue
            for var in d_sect.variables:
                try:
                    val = sect[var.name]
                except KeyError:
                    # Check if it's required.
                    if not var.has_default:
                        raise DoconfBadConfigError(
                            'cant find config variable {!r} in section {!r}'
                            .format(var.name, d_sect.name)
                        )
                    continue
                try:
                    val = parse_as(val, var.typ)
                except DoconfTypeError as e:
                    raise DoconfBadConfigError(
                        'variable {!r} cant be parsed as {!r} ({!r}): {}'
                        .format(var.name, var.typ, val, str(e))
                    )
                sect_values[var.name] = val

    def __getitem__(self, item):
        return self._values[item.lower()]

    def get(self, item, **kwargs):
        return self._values.get(item.lower(), **kwargs)

    def __contains__(self, item):
        return item.lower() in self._values
