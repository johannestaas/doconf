import re
import ast

from .exceptions import DoconfClassError, DoconfTypeError

RE_NAME = re.compile(r'^\s*[nN][aA][mM][eE]\s*:\s*(?P<name>\S+)\s*$')
RE_ENV = re.compile(r'^\s*\{(?P<env>[^\}]+)\}\s*$')
RE_SECT = re.compile(r'^\s*\[(?P<section>[^\]]+)\]\s*$')
RE_VAR = re.compile(
    r'^\s*(?P<id>\w+)\s*(\((?P<typestr>[^\)]+)\))?\s*:\s*(?P<desc>.*)$'
)


class _Env:
    def __init__(self, name):
        self.name = name.strip().lower()
        self.sections = []
        self.section_names = set()


class _Section:
    def __init__(self, name, env=None):
        self.name = name.strip().lower()
        self.variables = []
        self.variable_names = set()
        self.env = env
        self.has_required = False
        self.defaults = {}


class _Var:
    def __init__(
        self, name, default=None, has_default=False, typestr=None, desc=None,
        section=None,
    ):
        self.name = name.strip().upper()
        self.default = default
        self.has_default = has_default
        if typestr:
            self.typestr = typestr.strip().lower()
        self.section = section
        if typestr == 'int':
            self.typ = int
        elif typestr in ('str', 'string', None):
            self.typ = str
        elif typestr in ('bool', 'boolean'):
            self.typ = bool
        elif typestr == 'float':
            self.typ = float
        else:
            raise DoconfClassError('unknown type {!r}'.format(typestr))
        if self.has_default:
            self.default = parse_as(self.default, self.typ)
            self.section.defaults[self.name] = self.default
        else:
            self.section.has_required = True
        self.desc = desc


class _State:
    def __init__(self, lines):
        self.lines = [
            x.strip()
            for x in lines
            if not x.startswith('#') and x.strip()
        ]
        self.line_num = 0
        self.sect = None
        self.env = None
        self.envs = {}
        self.dct = {}

    @property
    def line(self):
        if self.line_num >= len(self.lines):
            return None
        return self.lines[self.line_num]

    def gen_lines(self):
        while self.line is not None:
            yield self.line
            self.line_num += 1
        self.line_num = 0

    def handle_name(self):
        m = RE_NAME.match(self.line)
        if m and self.sect is None:
            if '_NAME' in self.dct:
                raise DoconfClassError(
                    'duplicate name {!r} found before line:\n{!r}'
                    .format(self.dct['_NAME'], self.line)
                )
            else:
                self.dct['_NAME'] = m.group('name').lower().strip()
            return True
        return False

    def handle_env(self):
        m = RE_ENV.match(self.line)
        if m:
            if '_NAME' not in self.dct:
                raise DoconfClassError(
                    'Please specify "name: my_app", before line:\n{!r}'
                    .format(self.line)
                )
            env_name = m.group('env').lower().strip()
            if env_name in self.envs:
                raise DoconfClassError(
                    'duplicate environment {!r} found, before line:\n{!r}'
                    .format(env_name, self.line)
                )
            self.env = _Env(env_name)
            self.envs[env_name] = self.env
            return True
        return False

    def handle_sect(self):
        m = RE_SECT.match(self.line)
        if m:
            if '_NAME' not in self.dct:
                raise DoconfClassError(
                    'Please specify "name: my_app", then {{DEFAULT}} '
                    'before line:\n{!r}'.format(self.line)
                )
            elif 'default' not in self.envs:
                raise DoconfClassError(
                    'Please specify {{DEFAULT}} environment before line:\n{!r}'
                    .format(self.line)
                )
            name = m.group('section').lower().strip()
            if name in self.env.section_names:
                raise DoconfClassError(
                    '{!r} is already defined as a section'.format(name)
                )
            self.env.section_names.add(name)
            self.sect = _Section(name, env=self.env)
            self.env.sections.append(self.sect)
            return True
        return False

    def handle_var(self):
        m = RE_VAR.match(self.line)
        if m:
            if '_NAME' not in self.dct:
                raise DoconfClassError(
                    'Please specify "name: my_app", then {{DEFAULT}} then '
                    'a section like [section] before line:\n{!r}'
                    .format(self.line)
                )
            elif 'default' not in self.envs:
                raise DoconfClassError(
                    'Please specify {{DEFAULT}} environment and then [section] '
                    'before line:\n{!r}'.format(self.line)
                )
            elif self.sect is None:
                raise DoconfClassError(
                    'Please specify a section before line:\n{!r}'
                    .format(self.line)
                )
            name = m.group('id').upper().strip()
            if name in self.sect.variable_names:
                raise DoconfClassError('{!r} already specified in {!r}'.format(
                    name, self.sect.name,
                ))
            self.sect.variable_names.add(name)
            typestr = m.group('typestr')
            default = None
            has_default = False
            if typestr is None:
                typestr = 'str'
            elif ':' in typestr:
                typestr, default = typestr.split(':', 1)
                has_default = True
            desc = m.group('desc')
            var = _Var(
                name, default=default, has_default=has_default,
                typestr=typestr, desc=desc, section=self.sect,
            )
            self.sect.variables.append(var)
            return True
        return False

    def handle_multiline(self):
        line = self.line.strip()
        if line.startswith('>') and self.sect.variables:
            self.sect.variables[-1].desc += ' ' + self.line.lstrip('>').strip()
            return True
        return False


def parse_as(val, typ):
    val = val.strip()

    if val.lower() in ('null', 'none'):
        return None

    if val.lower() in ('true', 'false') and typ is bool:
        return ast.literal_eval(val.title())

    if typ is str:
        if (
            (val.startswith('"') and val.endswith('"')) or
            (val.startswith("'") and val.endswith("'"))
        ):
            return ast.literal_eval(val)
        else:
            return str(val)
    elif typ in (int, float, bool):
        try:
            val = ast.literal_eval(val)
        except ValueError:
            raise DoconfTypeError(
                'value {!r} unable to be eval\'ed as {!r}'.format(val, typ)
            )
        try:
            return typ(val)
        except ValueError:
            raise DoconfTypeError(
                'value {!r} unable to be coerced to {!r}'.format(val, typ)
            )

    raise DoconfTypeError(
        'can only parse type str, int, float, bool, not {!r}'.format(typ)
    )


def parse_docs(lines, dct):
    state = _State(lines)

    for line in state.gen_lines():
        if state.handle_name():
            continue
        if state.handle_env():
            continue
        if state.handle_sect():
            continue
        if state.handle_var():
            continue
        if state.handle_multiline():
            continue

    if not state.envs.get('default'):
        raise DoconfClassError('No DEFAULT configurations documented in class')

    dct['_ENVS'] = state.envs
    dct['_NAME'] = state.dct['_NAME']
