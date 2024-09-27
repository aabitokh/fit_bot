import logging


def get_logger():
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.DEBUG, filename='app.log',
        filemode='a',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s')
    return logger
