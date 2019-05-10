from doconf import DoconfConfig


class CustomConfig(DoconfConfig):
    '''
    name: my_example_app

    {DEFAULT}

    [server]
    HOST (str:"127.0.0.1"): the hostname of the server
    PORT (int:8080): the port number of the server
    DEBUG (bool:true): whether debug mode is on
    LOG_LEVEL (str:"debug"): the log level setting
    LOG_PATH (str:"./my_example_app.log"): the default log path

    [required_stuff]
    MAKE (str): the make of the car
    MODEL (str): the model of the car
    YEAR (int): the year the car was made
    ACCELERATION (float): how many seconds 0 to 60mph
    FOUR_DOORS (bool): whether it has four doors

    {PRODUCTION}

    [server]
    HOST (str:"0.0.0.0"): the hostname of the server
    PORT (int:8080): the port number of the server
    DEBUG (bool:false): whether debug mode is on
    LOG_LEVEL (str:"info"): the log level setting
    LOG_PATH (str:"/var/log/my_example_app.log"): the default log path

    [required_stuff]
    MAKE (str:"cadillac"): the make of the car
    MODEL (str:"deville"): the model of the car
    YEAR (int:1990): the year the car was made
    ACCELERATION (float:20.1): how many seconds 0 to 60mph
    FOUR_DOORS (bool:true): whether it has four doors

    '''
    pass
