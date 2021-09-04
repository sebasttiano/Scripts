import os
import logging
import config
import random
from aiogram import Bot, Dispatcher, executor, types


# log level
logging.basicConfig(level=logging.INFO)
# init bot
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)


async def _send_sticker(message: types.Message, name: str):
    with open(f'files/stickers/{name}.webp', 'rb') as sti:
        await message.answer_sticker(sti)


@dp.message_handler(commands=['start', 'welcome'])
async def welcome(message: types.Message):
    """ Welcome func. Welcomes with sticker"""
    await _send_sticker(message, 'welcome_gangs')
    me = await bot.get_me()

    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    buttons = ['Скока-скока адресов осталось?', 'Кого там ддудосят то?', 'Круглый жги!', 'TECT']
    markup.add(*buttons)

    await message.answer(f'Братуха {message.from_user.first_name}, чем тебе помочь?\nЯ - '
                         f'<b>{me.first_name}</b> если что', parse_mode='html', reply_markup=markup)


@dp.message_handler()
async def free_ip_num(message: types.Message) -> None:
    """Sends back information about free ip addresses"""
    pass

@dp.message_handler()
async def answer(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Скока-скока адресов осталось?':
            await message.answer("Порядком еще. Но это не точно")
        elif message.text == 'Кого там ддудосят то?':
            await message.answer('Да урода какого-то')
        elif message.text == 'Круглый жги!':
            await message.answer(kruglyi())
        else:
            await _send_sticker(message, random.choice(config.SUCHORUKOV_STICKERS))


def kruglyi():
    return random.choice(config.kruglyi_quotes)

# RUN
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)