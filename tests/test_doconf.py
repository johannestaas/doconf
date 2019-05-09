import os
import sys

rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [rootdir] + sys.path

from doconf import DoconfConfig


class BasicConfig(DoconfConfig):
    '''
    name: doconf_unittest

    {DEFAULT}

    [section1]
    DEBUG (bool): debug mode on or off
    AGE (int): person's age
    SUCCESS (float): how successful in parsing this config from 0 to 1
    NAME (str): the person's name
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
