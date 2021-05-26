"""Как сделать фильтрацию логов, чтобы можно было разные уровню логировать в разные источники.
Или получать логи от определенных функций"""
import logging.config
from settings import logger_config_filters

logging.config.dictConfig(logger_config_filters)

logger = logging.getLogger('app_logger')

def new_function():
    name = 'Sergey'
    # С помощью параметра extra можно передать в LogRecord доп.атрибут и его обработать
    logger.debug('Enter in to the new_function()',
                 extra={'user_name': name})


def main():
    # этот вывод зафильтрован
    logger.debug('Enter in to the main()')

if __name__ == '__main__':
    new_function()
    main()