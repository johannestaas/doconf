def main():
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')

    s = subs.add_subparser('find')

    s = subs.add_subparser('validate')

    s = subs.add_subparser('generate')

    args = parser.parse_args()


if __name__ == '__main__':
    main()
