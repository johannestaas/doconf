'''
doconf

Configuration specified through documentation, supporting multiple formats.
'''
from .config import DoconfConfig
from .exceptions import (
    DoconfError, DoconfClassError, DoconfFileError, DoconfTypeError,
)

__title__ = 'doconf'
__version__ = '0.0.1'
__all__ = (
    'DoconfConfig',
    'DoconfError',
    'DoconfClassError',
    'DoconfFileError',
    'DoconfTypeError',
)
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2019 Johan Nestaas'


def main():
    pass


if __name__ == '__main__':
    main()
