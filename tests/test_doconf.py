import os
import sys
import pytest

rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [rootdir] + sys.path

from doconf import (
    DoconfConfig,
    DoconfBadConfigError,
    DoconfClassError,
    DoconfTypeError,
    DoconfUndefinedEnvironmentError,
)


class BasicConfig(DoconfConfig):
    '''
    name: doconf_unittest

    {DEFAULT}

    [section1]
    DEBUG (bool:false): debug mode on or off
    AGE (int:20): person's age
    SUCCESS (float:1.0): how successful in parsing this config from 0 to 1
    NAME (str:greg): the person's name, and this is required
    IDEA (str:"fizz buzz bar"): some string with a default

    [second_section]
    DEBUG2 (bool:false): debug mode on or off
    AGE2 (int:333): person's age
    SUCCESS2 (float:1.0): how successful in parsing this config from 0 to 1
    NAME2 (str:"guydude"): the person's name
    IDEA2: something with no type or default
    '''
    pass


def test_load_basic_config():
    conf = BasicConfig.load(text='''
    # Comment 1
    [section1]
    # Comment 2
    DEBUG=true
    AGE=30
    SUCCESS=1
    NAME=joey
    [second_section]
    DEBUG2=true
    IDEA2=fazz bazz
    ''')
    assert conf['section1']['debug'] is True
    assert conf['section1']['age'] == 30
    assert conf['section1']['success'] == 1.0
    assert isinstance(conf['section1']['success'], float)
    assert conf['section1']['name'] == 'joey'
    assert conf['section1']['idea'] == 'fizz buzz bar'
    assert conf['second_section']['debug2'] is True
    assert conf['second_section']['idea2'] == 'fazz bazz'


def test_case_insensitivity():
    conf = BasicConfig.load(text='''
    [section1]
    DEBUG=true
    AGE=30
    SUCCESS=1
    NAME=joey
    # Should raise issue with IDEA missing...
    # IDEA=test
    [second_section]
    DEBUG2=true
    IDEA2=fazz bazz
    ''')
    from pprint import pprint
    pprint(conf._values)
    assert conf['SECTION1']['name'] == 'joey'
    assert conf['section1']['NAME'] == 'joey'
    assert conf['SECTION1']['NAME'] == 'joey'
    assert conf['section1']['name'] == 'joey'
    assert conf['Section1']['Name'] == 'joey'
    assert conf['SectioN1']['NamE'] == 'joey'
    assert conf['section1']['NaMe'] == 'joey'

    assert 'name' in conf['section1']
    assert 'NAME' in conf['section1']
    assert 'NaMe' in conf['section1']

    assert 'section1' in conf
    assert 'SECTION1' in conf
    assert 'sectION1' in conf


def test_all_defaults():
    conf = BasicConfig.load(text='''
    [second_section]
    IDEA2=asdf
    ''')
    sect = conf['section1']
    assert sect['DEBUG'] is False
    assert sect['AGE'] == 20
    assert sect['SUCCESS'] == 1.0 and isinstance(sect['SUCCESS'], float)
    assert sect['NAME'] == 'greg'
    assert sect['IDEA'] == 'fizz buzz bar'
    sect = conf['second_section']
    assert sect['DEBUG2'] is False
    assert sect['AGE2'] == 333
    assert sect['SUCCESS2'] == 1.0
    assert sect['NAME2'] == 'guydude'
    assert sect['IDEA2'] == 'asdf'


def test_missing_required():
    with pytest.raises(DoconfBadConfigError):
        BasicConfig.load(text='''[second_section]''')


def test_config_missing_name():
    with pytest.raises(DoconfClassError):
        class BadConfig(DoconfConfig):
            '''

            {DEFAULT}

            [section1]
            HOST (str:"127.0.0.1"): the hostname
            '''
            pass


def test_config_missing_env():
    with pytest.raises(DoconfClassError):
        class BadConfig(DoconfConfig):
            '''
            name: myapp
            [section1]
            HOST (str:"127.0.0.1"): the hostname
            '''
            pass


def test_config_missing_section():
    with pytest.raises(DoconfClassError):
        class BadConfig(DoconfConfig):
            '''
            name: myapp
            {DEFAULT}
            HOST (str:"127.0.0.1"): the hostname
            '''
            pass


def test_config_class_has_bad_type_default():
    with pytest.raises(DoconfTypeError):
        class BadConfig(DoconfConfig):
            '''
            name: myapp
            {DEFAULT}
            [section1]
            PORT (int:"foo"): foo is not a number
            '''
            pass
    with pytest.raises(DoconfTypeError):
        class BadConfig2(DoconfConfig):
            '''
            name: myapp
            {DEFAULT}
            [section1]
            PROGRESS (float:"foo"): foo is not a float
            '''
            pass


def test_multiple_envs():
    class GoodConfig(DoconfConfig):
        '''
        name: my_server

        {DEFAULT}
        [server]
        PORT (int:8080): server hosted on this port
        DEBUG (bool:true): debugging mode activate

        {STAGING}
        [server]
        PORT (int:8081): this port
        HOSTNAME (str:"staging.example.org"): this host

        {PRODUCTION}
        [server]
        PORT (int:8082): this port
        HOSTNAME (str:"production.example.org"): this production host
        DEBUG (bool:false): not debugging in prod
        '''
        pass

    default_conf = GoodConfig.load(env='default', text='')
    staging_conf = GoodConfig.load(env='staging', text='')
    prod_conf = GoodConfig.load(env='production', text='')

    assert default_conf['server']['port'] == 8080
    assert default_conf['server']['debug'] is True
    assert 'HOSTNAME' not in default_conf['server']

    assert staging_conf['server']['port'] == 8081
    assert staging_conf['server']['hostname'] == 'staging.example.org'
    assert 'DEBUG' not in staging_conf['server']

    assert prod_conf['server']['port'] == 8082
    assert prod_conf['server']['hostname'] == 'production.example.org'
    assert prod_conf['server']['debug'] is False


def test_load_bad_env():
    class GoodConfig(DoconfConfig):
        '''
        name: myserver

        {default}
        [server]
        PORT (int:8080): whatever

        {staging}
        [server]
        PORT (int:8080): whatever

        # No production defined yet.
        '''
        pass
    with pytest.raises(DoconfUndefinedEnvironmentError):
        GoodConfig.load(text='', env='production')
