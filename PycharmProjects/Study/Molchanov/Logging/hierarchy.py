import logging

# basicConfig() создает дефольтный обработчик у root логера
logging.basicConfig()
# logger = logging.getLogger()
# print(logger)

app_logger = logging.getLogger('app_logger')

console_handler = logging.StreamHandler()
app_logger.addHandler(console_handler)
# print(app_logger)
# print(app_logger.handlers)

# Создаем свой объект форматтера: levelname - аттрибут объекта LogRecord (уровень), name - имя логгера,
# message - сообщение
f = logging.Formatter(fmt='%(levelname)s - %(name)s - %(message)s')
console_handler.setFormatter(f)
print('Root handlers', app_logger.parent.handlers)

utils_logger = logging.getLogger('app_logger.utils')
utils_logger.setLevel('DEBUG')
# utils_logger.propagate = False

print(utils_logger)
print(utils_logger.handlers)


# root.app_logger.utils_logger
# Проверку уровня проводит только первый логер (например utils_logger, если у него нет обработчика,
# он передает наверх по иерархии(propagation) Такое поведение можно выключить, аттрибут propagate = False
def main():
    utils_logger.debug('Hello world')


if __name__ == '__main__':
    main()