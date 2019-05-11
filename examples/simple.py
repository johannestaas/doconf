from doconf import DoconfConfig


class SimpleConfig(DoconfConfig):
    '''
    name: simple_app

    # The environment
    {default}

    [main_section]
    HOST (str:"127.0.0.1"): who the server hosts the app to
    PORT (int:8080): the default port, defined as an integer with default 8080
    TIMEOUT (int): this is required because no default was defined
    MILES_PER_HOUR (int:null): this is NOT required and is default None
    DEBUG (bool:false): this is a boolean that is defaulting to False

    # We can continue to define new sections.
    [other_section]
    NAME: this variable has no type defined so it is a "str" and required
    AGE (int): this is an integer that is required. Due to this being required,
        > it will fail if this section doesn't exist. This is also a long
        > multiline description with continued lines specified with ">" prefix.

    [third_section]
    THIRD_SECT_VALUE (str:null): not required, default None
    '''
    pass


if __name__ == '__main__':
    # Since the config exists in the current directory, that's what will get
    # loaded.
    config = SimpleConfig.load()

    print('main_section')
    print('------------')
    print('HOST: {!r}'.format(config['main_section']['HOST']))
    print('PORT: {!r}'.format(config['main_section']['PORT']))
    print('TIMEOUT: {!r}'.format(config['main_section']['TIMEOUT']))
    print('MILES_PER_HOUR: {!r}'.format(config['main_section']['MILES_PER_HOUR']))
    print('DEBUG: {!r}'.format(config['main_section']['DEBUG']))
    print()

    print('other_section')
    print('-------------')
    print('NAME: {!r}'.format(config['other_section']['NAME']))
    print('AGE: {!r}'.format(config['other_section']['AGE']))
    print()

    print('third_section')
    print('-------------')
    print('THIRD_SECT_VALUE: {!r}'.format(
        config['third_section']['THIRD_SECT_VALUE'])
    )
