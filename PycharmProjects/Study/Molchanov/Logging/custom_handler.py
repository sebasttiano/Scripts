"""Создаем свой обработчик"""
import logging.config

from settings import logger_config_basic

logging.config.dictConfig(logger_config_basic)

logger = logging.getLogger('app_logger')

def main():
    logger.debug('Enter in to the main()')

if __name__ == '__main__':
    main()