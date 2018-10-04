import logging

#Change the format of logging message
fmt = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"

logging.basicConfig(level=logging.DEBUG, format=fmt, filename='access.log')

logging.debug('A debug note')
logging.info('Confirmation msg')
logging.warning('warning msg')
logging.error('Error note')
logging.critical('panic error')