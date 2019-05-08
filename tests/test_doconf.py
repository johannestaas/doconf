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
    IDEA: some default string

    [second_section]
    DEBUG2 (bool:false): debug mode on or off
    AGE2 (int:333): person's age
    SUCCESS2 (float:1.0): how successful in parsing this config from 0 to 1
    NAME2 (str:"guydude"): the person's name
    IDEA2: something with no type or default
    '''
    pass


def test_load_basic_config():
    BasicConfig.load(text='''
    [section1]
    DEBUG=true
    AGE=30
    SUCCESS=1
    NAME=joey
    # Should raise issue with IDEA missing...
    # IDEA=test
    [section2]
    DEBUG2=true
    ''')
