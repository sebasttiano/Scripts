""" Конфигурирование логирования в ручную"""
import logging

logger = logging.getLogger('app_logger')
# Уровень логера по умолчанию наследуется от root = WARNING
logger.setLevel('DEBUG')
# Определяем форматтер. С помощью параметра style можно заменить дефолтные %()s на что угодно
std_format = logging.Formatter(fmt='{asctime} - {levelname} - {name} - {message}', style='{')
# Уровень логера и обработчика должны быть ниже или равны уровню сообщения, чтобы произошло логирование
# Обработчик, который пишет в stderr
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

# Обработчик, который пишет в файл. параметр mode в данном случае дописывает строки ниже в файл
# a  - append
file_handler = logging.FileHandler('debug.log', mode='a')
logger.addHandler(file_handler)
file_handler.setFormatter(std_format)


console_handler.setFormatter(std_format)

def main():
    logger.debug('Enter in to the main()')

if __name__ == '__main__':
    main()