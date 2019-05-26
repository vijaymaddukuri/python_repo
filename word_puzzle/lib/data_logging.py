from os.path import dirname, abspath

import datetime
import logging as logger


def data_logging():
    """
    This function is to create the stream line handler for storing runtime logs
    """

    current_dir = dirname(dirname(abspath(__file__)))

    logfile = datetime.datetime.now().\
        strftime('word_puzzle_%H_%M_%d_%m_%Y.log')

    logpath = '{}/{}'.format(current_dir, logfile)

    logger.basicConfig(level=logger.INFO,
                       format='%(asctime)s %(levelname)-8s %(message)s',
                       datefmt='%m-%d %H:%M',
                       filename=logpath,
                       filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logger.StreamHandler()
    console.setLevel(logger.INFO)
    formatter = logger.Formatter('%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.getLogger('').addHandler(console)
