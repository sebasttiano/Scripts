import logging
import requests

logging.basicConfig(level="DEBUG")
logger = logging.getLogger()

logging.getLogger('urllib3').setLevel('CRITICAL')
def main(name):
    logger.debug(f'Enter in the main() function: name = {name}')

    r = requests.get('https://google.ru')

if __name__ == '__main__':
    main('Voron')