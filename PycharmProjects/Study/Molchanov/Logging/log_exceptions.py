"""Здесь показано, как логировать дополнительно и traceback"""
import logging.config
from settings import logger_config_exceptions

logging.config.dictConfig(logger_config_exceptions)

logger = logging.getLogger('app_logger')

words = ['new house', 'apple', 'ice cream', 3]

def main():
    for item in words:
        try:
            print(item.split(' '))
        except:
            # Можно передать в лог вывод traceback
            logger.exception(f'Exception here, item = {item}')
            # или так logger.debug(f'Exception here, item = {item}', exc_info=True)

if __name__ == '__main__':
    main()