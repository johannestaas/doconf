'''
doconf.exceptions
-----------------

Basic exception types for Doconf.
'''


class DoconfError(ValueError):
    '''
    Base Doconf exception.
    '''
    pass


class DoconfClassError(DoconfError):
    '''
    Class isn't documented properly.
    '''
    pass


class DoconfFileError(DoconfError):
    '''
    Config file not found or unreadable.
    '''
    pass


class DoconfTypeError(DoconfError):
    '''
    Config variable read is of wrong type.
    '''
    pass


class DoconfBadConfigError(DoconfError):
    '''
    Raised when configuration is missing required variables, or in general is
    in the wrong format.
    '''
    pass
