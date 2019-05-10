import os


def load_class(module, class_name):
    submod = __import__(module)
    for next_mod in module.split('.')[1:]:
        submod = getattr(submod, next_mod)
    cls = getattr(submod, class_name)
    return cls


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')

    s = subs.add_parser('find')
    s.add_argument('module', help='module containing class, eg: my_app.config')
    s.add_argument('class_name', help='the class with the doc string')

    s = subs.add_parser('validate')

    s = subs.add_parser('generate')

    args = parser.parse_args()

    if args.cmd == 'find':
        cls = load_class(args.module, args.class_name)
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
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
