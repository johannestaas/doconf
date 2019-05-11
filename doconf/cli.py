import os
import sys


def load_class(module, class_name):
    sys.path = ['.'] + sys.path
    submod = __import__(module)
    for next_mod in module.split('.')[1:]:
        submod = getattr(submod, next_mod)
    return getattr(submod, class_name)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')

    s = subs.add_parser(
        'find', help='find where the config file would be loaded from',
    )
    s.add_argument(
        'class_path',
        help=(
            'path to the module and class, '
            'eg: custom_example.config:CustomConfig'
        ),
    )

    s = subs.add_parser(
        'validate', help='validate your config files match the format',
    )
    s.add_argument(
        'class_path',
        help=(
            'path to the module and class, '
            'eg: custom_example.config:CustomConfig'
        ),
    )
    s.add_argument('--config-path', '-c', help='direct path to config')
    s.add_argument(
        '--env', '-e', default='default', help='the environment to use',
    )

    s = subs.add_parser(
        'generate', help='generate example config files',
    )
    s.add_argument(
        'class_path',
        help=(
            'path to the module and class, '
            'eg: custom_example.config:CustomConfig'
        ),
    )
    s.add_argument(
        '--out', '-o', default='.',
        help='output directory, default to current directory',
    )

    args = parser.parse_args()

    if ':' not in getattr(args, 'class_path', ''):
        parser.print_usage()
        print()
        print('You need to pass the class name in the class path, like: ')
        print('my_app.config:MyConfigClass')
        sys.exit(1)
    else:
        module, class_name = args.class_path.split(':', 1)
        cls = load_class(module, class_name)

    if args.cmd == 'find':
        paths = cls.possible_paths()
        first = None
        print('Would look at these paths, and found these files:\n')
        for path in paths:
            exists = os.path.isfile(path)
            if first is None and exists:
                first = path
            print('{} {}'.format('[*]' if exists else '[ ]', path))
        print()
        if first is None:
            print('None found!')
        else:
            print('Would have loaded: {}'.format(first))
    elif args.cmd == 'validate':
        conf = cls.load(path=args.config_path, env=args.env)
        for sect_name in conf._values.keys():
            sect_title = 'Section {!r}'.format(sect_name)
            sect_title = '{}\n{}'.format(sect_title, '-' * len(sect_title))
            print(sect_title)
            sect = conf[sect_name]
            for key, val in sorted(sect.items()):
                print('{} ({}) = {!r}'.format(
                    key, val.__class__.__name__, val,
                ))
            print()
    elif args.cmd == 'generate':
        for env_name, env in cls._ENVS.items():
            filename = '{}.{}.config'.format(
                env_name.lower(), cls._NAME.lower(),
            )
            path = os.path.join(args.out, filename)
            text = ''
            for sect in env.sections:
                text += '[{}]\n'.format(sect.name)
                for var in sect.variables:
                    extra = '# ({}) '.format(var.typ.__name__)
                    desc = var.desc.split()
                    while desc:
                        x = len(extra) // 80
                        y = len('{} {}'.format(extra, desc[0])) // 80
                        if y > x:
                            extra += '\n# {}'.format(desc[0])
                        else:
                            extra += ' {}'.format(desc[0])
                        desc = desc[1:]
                    text += extra + '\n'
                    if var.has_default:
                        text += '{}={}\n'.format(var.name, var.default)
                    else:
                        text += '{}=<required>\n'.format(var.name)
                text += '\n'
            with open(path, 'w') as f:
                f.write(text)
            print('Dumped example to {}'.format(path))
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
