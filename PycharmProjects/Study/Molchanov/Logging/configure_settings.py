""" Конфигурирование логирования с помощью файла settings.py"""
import logging.config
from settings import logger_config_basic

# Подключаем словарь с настройками (
logging.config.dictConfig(logger_config_basic)
logger = logging.getLogger('app_logger')


def main():
    logger.debug('Enter in to the main()')

if __name__ == '__main__':
    main()