'''
doconf

Configuration specified through documentation, supporting multiple formats.
'''
from .cli import main
from .config import DoconfConfig
from .exceptions import (
    DoconfError, DoconfClassError, DoconfFileError, DoconfTypeError,
    DoconfBadConfigError, DoconfUndefinedEnvironmentError,
)

__title__ = 'doconf'
__version__ = '0.2.0'
__all__ = (
    'DoconfConfig',
    'DoconfError',
    'DoconfClassError',
    'DoconfFileError',
    'DoconfTypeError',
    'DoconfBadConfigError',
    'DoconfUndefinedEnvironmentError',
)
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2019 Johan Nestaas'


if __name__ == '__main__':
    main()
