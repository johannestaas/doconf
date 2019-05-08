'''
doconf.config
-------------

Core doconf logic lies here.
'''
import os
import re
from configparser import ConfigParser

from .exceptions import DoconfClassError, DoconfFileError, DoconfTypeError


RE_NAME = re.compile(r'^\s*[nN][aA][mM][eE]\s*:\s*(?P<name>\S+)\s*$')
RE_ENV = re.compile(r'^\s*\{(?P<env>[^\}]+)\}\s*$')
RE_SECT = re.compile(r'^\s*\[(?P<section>[^\]]+)\]\s*$')
RE_VAR = re.compile(
    r'^\s*(?P<id>\w+)\s+(\((?P<typestr>[^\)]+)\))?\s*:\s*(?P<desc>.*)$'
)


class _Env:
    def __init__(self, name):
        self.name = name
        self.sections = []
        self.section_names = set()


class _Section:
    def __init__(self, name):
        self.name = name
        self.variables = []
        self.variable_names = set()


class _Var:
    def __init__(
        self, name, default=None, has_default=False, typestr=None, desc=None,
    ):
        self.name = name
        self.default = default
        self.has_default = has_default
        self.typestr = typestr.strip().lower()
        if typestr == 'int':
            self.typ = int
        elif typestr in ('str', 'string'):
            self.typ = str
        elif typestr in ('bool', 'boolean'):
            self.typ = bool
        elif typestr == 'float':
            self.typ = float
        else:
            raise DoconfClassError('unknown type {!r}'.format(typestr))
        if self.has_default:
            self.default = parse_as(self.default, self.typ)
        self.desc = desc


def parse_as(val, typ):
    if typ in (str, int, float):
        return typ(val)
    if typ is bool:
        if isinstance(val, str):
            truthy = val.strip().lower() in ('true', 'on', 'yes', '1')
            falsey = val.strip().lower() in ('false', 'off', 'no', '0', 'null')
            if truthy:
                return True
            if falsey:
                return False
            raise DoconfTypeError(
                '{!r} not one of: (true, on, yes, 1, false, off, no, 0, null)'
                .format(val)
            )
        elif val in (True, False):
            return val
        elif val is None:
            return False
        elif isinstance(val, (int, float)):
            return val != 0
        else:
            raise DoconfTypeError('unknown type of {!r}'.format(val))
    raise DoconfTypeError(
        'can only parse type str, int, float, bool, not {!r}'.format(typ)
    )


def parse_docs(lines, dct):
    lines = [
        x.strip()
        for x in lines
        if not x.startswith('#') and x.strip()
    ]

    sect = None
    env = _Env('default')
    envs = {'default': env}

    for line in lines:

        m = RE_NAME.match(line)
        if m and sect is None:
            if '_NAME' in dct:
                raise DoconfClassError('duplicate `name: <name>` specified')
            else:
                dct['_NAME'] = m.group('name')
            continue

        m = RE_ENV.match(line)
        if m:
            if '_NAME' not in dct:
                raise DoconfClassError('specify `name: <name>` before env')
            env_name = m.group('env').upper()
            if env_name in envs:
                raise DoconfClassError(
                    '{!r} environment already specified'.format(env_name)
                )
            env = _Env(env_name)
            envs[env_name] = env
            continue

        m = RE_SECT.match(line)
        if m:
            if '_NAME' not in dct:
                raise DoconfClassError(
                    'specify `name: <name>` before sections'
                )
            name = m.group('section').lower()
            if name in env.section_names:
                raise DoconfClassError(
                    '{!r} is already defined as a section'.format(name)
                )
            env.section_names.add(name)
            sect = _Section(name)
            env.sections.append(sect)
            continue

        m = RE_VAR.match(line)
        if m:
            if '_NAME' not in dct:
                raise DoconfClassError('specify `name: <name>` first')
            name = m.group('id').strip().upper()
            if name in sect.variable_names:
                raise DoconfClassError('{!r} already specified in {!r}'.format(
                    name, sect.name,
                ))
            sect.variable_names.add(name)
            typestr = m.group('typestr')
            default = None
            has_default = False
            if ':' in typestr:
                typestr, default = typestr.split(':', 1)
                has_default = True
            desc = m.group('desc')
            var = _Var(
                name, default=default, has_default=has_default,
                typestr=typestr, desc=desc,
            )
            sect.variables.append(var)
            continue

    if not envs['default'].sections:
        del envs['default']
    if not envs:
        raise DoconfClassError('No configurations documented in class')

    dct['_ENVS'] = envs


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


class DoconfConfig(metaclass=MetaConfig):

    @classmethod
    def load(cls, path=None, text=None):
        config = ConfigParser()
        if text:
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
        return cls(config=config)

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

    def __init__(self, config=None):
        self._config = config
