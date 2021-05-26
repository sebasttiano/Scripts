"""Здесь хранятся настройки логирования в словаре. Можно сделать и в yaml виде"""
import logging

# свой обработчик, который будет записывать логи в файл
class MegaHandler(logging.Handler):
    def __init__(self, filename):
        logging.Handler.__init__(self)
        self.filename = filename

    # этот метод непосредственно и производит действие с логом. ему передается объект LogRecord
    def emit(self, record):
        message = self.format(record)
        with open(self.filename, 'a') as file:
            file.write(message + '\n')


# record - это объект LogRecord. нужно именно так создавать фильтр
class NewFunctionFilter(logging.Filter):
    def filter(self, record):
        # Если возвращатся True, то лог записывается, иначе нет.
        return record.funcName == 'new_function'

logger_config_basic = {
    'version': 1,
    'disable_existing_loggers': False, # Выключает все логгеры, кроме root
    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
        },
        #Свой созданный обработчик добавляем
        'myhandler': {
            # Инициализация класса
            '()': MegaHandler,
            'level': 'DEBUG',
            'filename': 'debug.log',
            'formatter': 'std_format'
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'myhandler']
            #'propagate': False
        }
    }
}

logger_config_filters = {
    'version': 1,
    'disable_existing_loggers': False, # Выключает все логгеры, кроме root
    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
            'filters': ['new_filter']
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['console']
            #'propagate': False
        }
    },
    'filters': {
        'new_filter': {
            # с помощью () мы говорим logging, чтобы он создал экземпляр нужного нам класса. Также его надо подключить
            # к обработчику в ключе filters
            '()': NewFunctionFilter   # путь до класса. Если бы он был описан в filters.pu: filters.NewFunctionFilter
        }
    },
    # 'root': {} # '': {},
    # 'incremental': True  # Это говорит, что этот конфиг является дополнительной
}

logger_config_exceptions = {
    'version': 1,
    'disable_existing_loggers': False, # Выключает все логгеры, кроме root
    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} -'
                      ' {module}:{funcName}:{lineno} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format'
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['console']
            #'propagate': False
        }
    }
    # 'filters': {},
    # 'root': {} # '': {},
    # 'incremental': True  # Это говорит, что этот конфиг является дополнительной
}